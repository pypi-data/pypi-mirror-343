import hashlib
import shutil
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from onnx import mapping, TensorProto
import numpy as np
import onnx
import onnxruntime as ort
import torch
from onnx import numpy_helper
from runlocal_tools.backend.ml_model import Model
from runlocal_tools.dtypes.upload import UploadedModelType


class OnnxModel(Model):
    model_type: UploadedModelType = UploadedModelType.ONNX
    model: Optional[onnx.ModelProto] = None
    compiled_model: Optional[ort.InferenceSession] = None
    temp_dir: Optional[Path] = None
    device: str  # CPU, ...

    input_dict: Optional[Dict[str, np.ndarray]] = None
    output_dict: Optional[Dict[str, np.ndarray]] = None

    def __init__(
        self,
        model_path: Optional[Path],
        temp_dir: Optional[Path],
        should_compile: bool = True,
        should_load: bool = True,
        loaded_model: Optional[onnx.ModelProto] = None,
        device: str = "CPU",
    ):
        super().__init__()

        self.model_path = model_path
        self.onnx_model_path = model_path

        if self.model_path and self.model_path.is_dir():
            for file in self.model_path.iterdir():
                if file.suffix == ".onnx":
                    self.onnx_model_path = file

        self.temp_dir = temp_dir
        self.device = device

        if loaded_model is not None:
            self.model = loaded_model
        elif self.onnx_model_path is not None:
            self.model = onnx.load_model(self.onnx_model_path)

        # code to modify the model proto to have f16 outputs, due to bug in ONNXRuntime, now monkeypatched.
        # for output in self.model.graph.output:
        #     if output.name == "output":  # adjust if the name differs
        #         sequence_type = onnx.TypeProto.Sequence()
        #         # Suppose you want the sequence to contain tensors of FLOAT16
        #         tensor_type = sequence_type.elem_type.tensor_type
        #         tensor_type.elem_type = TensorProto.FLOAT16
        #         output.type.Clear()  # Clears any previously set type (tensor, sequence, etc.)
        #         output.type.sequence_type.CopyFrom(sequence_type)

        # same thing in ONNXModel
        if should_load:
            self.load_compiled_model()
        if should_compile:
            self.load_compiled_model()

        self.input_type_dict = self.get_input_type_dict()

    def __enter__(self) -> "OnnxModel":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.destroy()

    def destroy(self) -> None:
        self.compiled_model = None
        self.model = None
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def is_compiled(self) -> bool:
        return self.compiled_model is not None

    def get_input_type_dict(self) -> dict[str, np.dtype]:
        d = {}
        for input_info in self.model.graph.input:
            # Get the element type (an integer)
            elem_type = input_info.type.tensor_type.elem_type
            # Map it to a numpy type
            np_type = mapping.TENSOR_TYPE_TO_NP_TYPE[elem_type]
            # print(f"Input Name: {input_info.name}, Type: {np_type}")
            d[input_info.name] = np_type
        return d

    @staticmethod
    def extract_onnx_and_external_data_paths(model_path: Path) -> tuple[Path, Path]:
        # Find all .xml and .bin files in the directory
        onnx_files = list(model_path.glob("*.onnx"))
        external_data_files = [
            file for file in model_path.iterdir() if file.suffix != ".onnx"
        ]

        # Ensure there's exactly one .xml and one .bin file
        if len(onnx_files) != 1 or len(external_data_files) != 1:
            raise FileNotFoundError(
                "The directory must contain exactly one .xml file and one .bin file."
            )

        onnx_path = Path(onnx_files[0])
        external_data_path = Path(external_data_files[0])
        return onnx_path, external_data_path

    @staticmethod
    def calculate_hash(model_path: Path) -> str:
        hash_md5 = hashlib.md5()
        if model_path.is_file():
            with open(model_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        else:
            onnx_path, external_data_path = (
                OnnxModel.extract_onnx_and_external_data_paths(model_path)
            )
            # Iterate over the files and update the hash
            for file_path in [onnx_path, external_data_path]:
                with file_path.open("rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)

        return hash_md5.hexdigest()

    @staticmethod
    def from_loaded_model(model: onnx.ModelProto) -> "OnnxModel":
        return OnnxModel(
            model_path=None,
            temp_dir=None,
            should_compile=False,
            should_load=False,
            loaded_model=model,
            device="CPU",
        )

    @staticmethod
    def from_path(
        model_path: Path,
        temp_dir: Optional[Path] = None,
        should_compile: bool = False,
        should_load: bool = True,
        device: str = "CPU",
    ) -> Optional["OnnxModel"]:
        return OnnxModel(
            model_path=model_path,
            temp_dir=temp_dir,
            should_compile=should_compile,
            should_load=should_load,
            device=device,
        )

    def get_input_keys(self) -> List[str]:
        if self.model is not None:
            return [input.name for input in self.model.graph.input]

        return []

    def get_output_keys(self) -> List[str]:
        # May not return the expected output keys, since ONNX can combine multiple outputs into a single key
        # output key is defined in the OnnxConversionPipeline in `self.placeholder_output_name`
        if self.model is not None:
            return [output.name for output in self.model.graph.output]

        return []

    def get_input_shape(self, index: int = 0) -> List[int]:
        if self.model is not None:
            return [
                dim.dim_value
                for dim in self.model.graph.input[index].type.tensor_type.shape.dim
            ]
        return []

    def get_output_shape(self, index: int = 0) -> List[int]:
        if self.model is not None:
            return [
                dim.dim_value
                for dim in self.model.graph.output[index].type.tensor_type.shape.dim
            ]
        return []

    def load_model(self, compile: bool = False, force: bool = False):
        """
        load the model and set to self.model.
        If model is already loaded, do nothing
        """

        if compile:
            self.load_compiled_model(force=force)
        else:
            if not force and self.model is not None:
                return

            if self.onnx_model_path is None:
                raise ValueError("model_path is None - cannot compile")

            self.model = onnx.load_model(self.model_path)

    def load_compiled_model(self, force: bool = False):
        """
        If you want to compile the model after class initialization
        """
        if not force and self.compiled_model is not None:
            return

        if self.onnx_model_path is None:
            raise ValueError("model_path is None - cannot compile")

        # set the execution provider using the compute unit
        provider_config = self.map_compute_unit_to_execution_provider_config(
            self.device
        )
        provider_name = (
            provider_config if isinstance(provider_config, str) else provider_config[0]
        )
        providers = [
            # even if I don't put CPU, it will still fallback
            provider_config
        ]

        # self.compiled_model = ort.InferenceSession(self.onnx_model_path, providers=providers)
        self.compiled_model = ort.InferenceSession(
            self.model.SerializeToString(), providers=providers
        )
        compiled_providers: list[str] = self.compiled_model.get_providers()
        if provider_name not in compiled_providers:
            raise ValueError(
                f"Provider {provider_name} not in compiled providers: {compiled_providers} -- raising an error to be safe"
            )

    def reload(self):
        if self.onnx_model_path is None:
            raise ValueError("model_path is None - cannot load")

        self.model = onnx.load_model(self.onnx_model_path)

    def set_input(self, input: np.ndarray, index: int = 0) -> None:
        if self.model is not None:
            if self.input_dict is None:
                self.input_dict = {}
            input_key = self.get_input_keys()[index]
            self.input_dict[input_key] = input

    def execute(self, input_dict: dict) -> Dict[str, np.ndarray]:
        if self.compiled_model is not None:
            output_keys = self.get_output_keys()

            # cast input dict to the correct type
            for key, value in input_dict.items():
                input_dict[key] = value.astype(self.input_type_dict[key])

            outputs = self.compiled_model.run(None, input_dict)

            output_dict = {}
            for key, value in zip(output_keys, outputs):
                output_dict[key] = value

            return output_dict

        return {}

    def prepare_inputs(
        self, torch_inputs: List[torch.Tensor], model_input_keys: list[str]
    ) -> Dict[str, np.ndarray]:
        """
        Convert list of tensors to numpy float32 dict
        Not doing this inside execute() because that function will be benchmarked
        model_input_keys should be decided by the pipeline, because the ordering matters...
        i.e. the if you do get_input_keys() you may get a different ordering
        """
        numpy_inputs = [
            input_tensor.cpu().detach().numpy().astype(np.float32)
            for input_tensor in torch_inputs
        ]
        # input_keys = self.get_input_keys()
        input_keys = model_input_keys
        input_dict = dict(zip(input_keys, numpy_inputs))
        return input_dict

    def prepare_outputs(
        self, model_output: Any, model_output_keys: list[str]
    ) -> List[torch.Tensor]:
        """
        Convert model output to list of torch tensors. Needed for ModelPipeline integration
        Not doing this inside execute() because that function will be benchmarked
        CoreML output is a numpy dict
        """
        # first, check if model output contains multiple keys, because this is NOT the expected behaviour of ONNX
        # UPDATE: it appears ONNX actually exported a model with multiple keys, so the logic below will no longer work.

        # if model_output length = 1, check if the type is a sequence, if so, unpack it
        if len(model_output) == 1 and isinstance(
            model_output[list(model_output.keys())[0]], (list, tuple)
        ):
            # whereas CoreML will unpack the tensors if tuple, ONNX will not, all outputs will be in a list, in a single key
            output_key = list(model_output.keys())[0]
            torch_outputs = [torch.from_numpy(x) for x in model_output[output_key]]
            return torch_outputs

        elif len(model_output) == 1 and isinstance(
            model_output[list(model_output.keys())[0]], np.ndarray
        ):
            output_key = list(model_output.keys())[0]
            torch_outputs = [torch.from_numpy(model_output[output_key])]
            return torch_outputs

        # if more than 1 key, make sure each key is a single numpy array
        elif len(model_output) > 1:
            torch_outputs = [torch.from_numpy(x) for x in model_output.values()]
            return torch_outputs

        else:
            raise ValueError("Unexpected model output format")

    def get_opset_version(self) -> int:
        for opset in self.model.opset_import:
            domain = opset.domain if opset.domain != "" else "default"
            return opset.version
        raise ValueError("No opset version found")

    def map_compute_unit_to_execution_provider_config(
        self, compute_unit: str
    ) -> str | tuple:
        """maps a compute unit string to the ExecutionProvider config for the ORT session"""
        if compute_unit == "CPU" or compute_unit == "DEFAULT":
            return "CPUExecutionProvider"

        if compute_unit.startswith("CoreML"):
            coreml_compute_unit = compute_unit.split(";")[1]
            return (
                "CoreMLExecutionProvider",
                {
                    "ModelFormat": "MLProgram",
                    "MLComputeUnits": coreml_compute_unit,
                    "RequireStaticInputShapes": "0",
                    "EnableOnSubgraphs": "0",
                },
            )

        if compute_unit == "XNNPACK":
            return "XnnpackExecutionProvider"

        if compute_unit == "CUDA":
            return ("CUDAExecutionProvider", {"use_tf32": 0})

        raise ValueError(f"Unsupported compute unit: {compute_unit}")

    def get_weights_array_dict(self) -> Dict[str, np.ndarray]:
        weight_dict = {
            init.name: numpy_helper.to_array(init)
            for init in self.model.graph.initializer
        }
        return weight_dict

    @staticmethod
    def rename_feature(
        model,  # onnx model
        old_name: Optional[str],
        new_name: str,
        rename_inputs: bool,
        rename_outputs: bool,  # False to ignore outputs
    ):
        import onnxscript.ir

        model_ir = onnxscript.ir.from_proto(model)
        if rename_inputs and rename_outputs:
            raise ValueError("Cannot rename both inputs and outputs")
        if old_name is None:
            if rename_inputs:
                assert len(model_ir.graph.inputs) == 1, (
                    "Only 1 input allowed if old_name is None"
                )
                old_name = model_ir.graph.inputs[0].name
            elif rename_outputs:
                assert len(model_ir.graph.outputs) == 1, (
                    "Only 1 output allowed if old_name is None"
                )
                old_name = model_ir.graph.outputs[0].name
        if rename_inputs:
            for input in model_ir.graph.inputs:
                if input.name == old_name:
                    input.name = new_name
            if new_name not in [input.name for input in model_ir.graph.inputs]:
                raise ValueError(f"Input with name {old_name} not found")
        if rename_outputs:
            for output in model_ir.graph.outputs:
                if output.name == old_name:
                    output.name = new_name
            if new_name not in [output.name for output in model_ir.graph.outputs]:
                raise ValueError(f"Output with name {old_name} not found")
        renamed_model = onnxscript.ir.to_proto(model_ir)
        return renamed_model


    @staticmethod
    def set_input_name_and_shape(model, input_shapes: Dict[str, Tuple[int, ...]]):
        # Check if number of inputs matches the provided input shapes.
        if len(model.graph.input) != len(input_shapes):
            raise ValueError(
                "The number of input shapes provided does not match the number of model inputs."
            )

        # Iterate over inputs and corresponding provided shapes (order is preserved in Python 3.7+)
        for input_proto, (new_name, new_shape) in zip(
            model.graph.input, input_shapes.items()
        ):
            old_name = input_proto.name

            # Extract original dimensions: if dynamic (using dim_param) or missing, treat as -1.
            original_dims = []
            for d in input_proto.type.tensor_type.shape.dim:
                if d.HasField("dim_value"):
                    original_dims.append(d.dim_value)
                elif d.HasField("dim_param"):
                    original_dims.append(-1)
                else:
                    original_dims.append(-1)

            # Verify that the number of dimensions is the same.
            if len(original_dims) != len(new_shape):
                raise ValueError(
                    f"Input shape for '{old_name}' expected {len(original_dims)} dimensions, but got {len(new_shape)}."
                )

            # Verify each dimension:
            for i, (orig_dim, new_dim) in enumerate(zip(original_dims, new_shape)):
                if orig_dim != -1 and orig_dim != new_dim:
                    raise ValueError(
                        f"Input shape mismatch at dimension {i} for '{old_name}': expected {orig_dim}, but got {new_dim}."
                    )

            # Clear existing shape dims and set new shape.
            del input_proto.type.tensor_type.shape.dim[:]
            for dim in new_shape:
                new_dim_proto = input_proto.type.tensor_type.shape.dim.add()
                new_dim_proto.dim_value = dim

            # Rename the input.
            input_proto.name = new_name

            # Update any initializers that reference the old input name.
            for initializer in model.graph.initializer:
                if initializer.name == old_name:
                    initializer.name = new_name

            # Update any node that references the old input name.
            for node in model.graph.node:
                # Update node inputs.
                for idx, node_input in enumerate(node.input):
                    if node_input == old_name:
                        node.input[idx] = new_name
                # Update node outputs (if any use the same name).
                for idx, node_output in enumerate(node.output):
                    if node_output == old_name:
                        node.output[idx] = new_name
        inferred_model = onnx.shape_inference.infer_shapes(model)
        return inferred_model
