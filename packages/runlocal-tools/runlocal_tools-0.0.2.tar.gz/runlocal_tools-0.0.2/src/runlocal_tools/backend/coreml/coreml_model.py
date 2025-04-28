import hashlib
import shutil
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import coremltools.optimize.coreml as cto
import PIL
import coremltools as ct
import numpy as np
import torch
from pydantic import BaseModel

from runlocal_tools.backend.ml_model import Model
from runlocal_tools.dtypes.upload import UploadedModelType

class CoreMLAvailability(BaseModel):
    iOS: str
    macOS: str
    CoreML: str


def get_availability_mapping(spec_version: int) -> CoreMLAvailability:
    version_map = {
        1: CoreMLAvailability(iOS="iOS 11", macOS="macOS 10.13", CoreML="Core ML 1"),
        2: CoreMLAvailability(
            iOS="iOS 11.2", macOS="macOS 10.13.2", CoreML="Core ML 1.2"
        ),
        3: CoreMLAvailability(iOS="iOS 12", macOS="macOS 10.14", CoreML="Core ML 2"),
        4: CoreMLAvailability(iOS="iOS 13", macOS="macOS 10.15", CoreML="Core ML 3"),
        5: CoreMLAvailability(iOS="iOS 14", macOS="macOS 11", CoreML="Core ML 4"),
        6: CoreMLAvailability(iOS="iOS 15", macOS="macOS 12", CoreML="Core ML 5"),
        7: CoreMLAvailability(iOS="iOS 16", macOS="macOS 13", CoreML="Core ML 6"),
        8: CoreMLAvailability(iOS="iOS 17", macOS="macOS 14", CoreML="Core ML 7"),
        9: CoreMLAvailability(iOS="iOS 18", macOS="macOS 15", CoreML="Core ML 8"),
    }
    if spec_version not in version_map:
        raise ValueError(f"CoreML version {spec_version} not supported")
    return version_map[spec_version]


class CoreMLModel(Model):
    model: Optional[ct.models.MLModel] = None
    compiled_model: Optional[ct.models.CompiledMLModel] = None
    compiled_model_path: Optional[Path] = None
    model_type: UploadedModelType
    model_path: Path  # path to actual model
    temp_dir: Path
    compute_units: ct.ComputeUnit
    # basically the stem of the model package
    model_name: str

    input_dict: Optional[Dict[str, np.ndarray]] = None
    output_dict: Optional[Dict[str, np.ndarray]] = None

    def __init__(
        self,
        model_path: Path,
        model_type: UploadedModelType,
        temp_dir: Optional[Path],
        should_compile: bool = False,
        should_load: bool = True,
        compute_units: ct.ComputeUnit = ct.ComputeUnit.ALL,
        upload_id: Optional[
            str
        ] = None,  # added later, needed for multimodel activation compression
        make_state: Optional[bool] = False, # for stateful models
    ):
        super().__init__()
        """
        if should_load is False, then should_compile is ignored. Needed because Linux does not have CoreML compiler
        if temp_dir is None, then it won't be cleaned up
        Used if your model doesn't live in temp dir
        MLModels cannot be compiled like MLPackages
        """
        self.temp_dir = temp_dir
        self.model_type = model_type
        self.compute_units = compute_units
        self.model_name = model_path.stem
        self.upload_id = upload_id
        self.make_state = make_state
        self.coreml_state = None # set in load_model, if make_state is True

        if model_type in (UploadedModelType.MLPACKAGE, UploadedModelType.MLMODEL):
            self.model_path = model_path

            if should_load:
                self.load_model()
                if should_compile:
                    if self.temp_dir is None:
                        self.temp_dir = Path(tempfile.mkdtemp())
                    self.save_compiled_model_dir()
                    self.load_compiled_model()

        elif model_type == UploadedModelType.MLMODELC:
            if should_load:
                model = ct.models.CompiledMLModel(
                    str(model_path), compute_units=compute_units
                )
                self.compiled_model = model
                self.compiled_model_path = model_path
            else:
                self.compiled_model_path = model_path
        else:
            raise ValueError(f"Model type {model_type} not supported")

    def __enter__(self) -> "CoreMLModel":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # using context manager because MLModel needs the files on disk to work
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def is_compiled(self) -> bool:
        return self.compiled_model is not None

    def destroy(self) -> None:
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def save_compiled_model_dir(self):
        """
        copy the compiled model directory to a location first
        before benchmarking loading time
        """
        model_name = self.model_path.stem
        compiled_model_path = self.model.get_compiled_model_path()
        self.compiled_model_path = self.temp_dir / f"{model_name}.mlmodelc"
        shutil.move(compiled_model_path, str(self.compiled_model_path))

    def load_model(
        self,
        compile: bool = False,
        force: bool = False,
    ):
        """
        load the model and set to self.model. If model is already loaded, do nothing
        """
        if force or self.model is None:
            self.model = ct.models.MLModel(
                str(self.model_path), compute_units=self.compute_units
            )
            if self.make_state:
                self.coreml_state = self.model.make_state()

        if compile:
            self.save_compiled_model_dir()

    def load_compiled_model(
        self,
        force: bool = False,
    ):
        """
        If you want to compile the model after class initialization
        """
        if self.model is None:
            raise ValueError("Model must be loaded to use load_compiled_model")

        self.compiled_model = ct.models.CompiledMLModel(
            str(self.compiled_model_path), compute_units=self.compute_units
        )

    def get_input_keys(self) -> List[str]:
        input_keys = []
        if self.model is not None:
            spec = self.model.get_spec()
            for input_feature in spec.description.input:
                name = input_feature.name
                input_keys.append(name)
        return input_keys

    def get_output_keys(self) -> List[str]:
        output_keys = []
        if self.model is not None:
            spec = self.model.get_spec()
            for output_feature in spec.description.output:
                name = output_feature.name
                output_keys.append(name)
        return output_keys

    def get_input_shape(self, index: int = 0) -> List[int]:
        if self.model is not None:
            spec = self.model.get_spec()
            input_feature = spec.description.input[index]
            return input_feature.type.multiArrayType.shape
        return []

    def get_output_shape(self, index: int = 0) -> List[int]:
        if self.model is not None:
            spec = self.model.get_spec()
            output_feature = spec.description.output[index]
            return output_feature.type.multiArrayType.shape
        return []

    def execute(self, input_dict: Dict) -> Dict[str, np.ndarray]:
        """
        inputs should already be in numpy
        """
        predict_fn = None
        if self.compiled_model:
            predict_fn = self.compiled_model.predict
        elif self.model:
            predict_fn = self.model.predict

        if self.coreml_state:
            output_dict = predict_fn(
                data=input_dict,
                state=self.coreml_state,
            )
        else:
            output_dict = predict_fn(input_dict)
        return output_dict

    @staticmethod
    def calculate_hash(model_path: Path, model_type: UploadedModelType) -> str:
        # the coremldata.bin file is a binary file that is generated by the compiler and is not deterministic.
        # We will not include it in the hash calculation
        if model_type == UploadedModelType.MLMODELC:
            hash_md5 = hashlib.md5()
            weight_path = model_path / "weights" / "weight.bin"
            model_mil_path = model_path / "model.mil"
            analytics_path = model_path / "analytics" / "coremldata.bin"
            for file_path in [weight_path, model_mil_path, analytics_path]:
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
            return hash_md5.hexdigest()
        elif model_type == UploadedModelType.MLPACKAGE:
            hash_md5 = hashlib.md5()
            mlmodel_path = model_path / "Data" / "com.apple.CoreML" / "model.mlmodel"
            weight_path = (
                model_path / "Data" / "com.apple.CoreML" / "weights" / "weight.bin"
            )
            for file_path in [weight_path, mlmodel_path]:
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
            return hash_md5.hexdigest()
        elif model_type == UploadedModelType.MLMODEL:
            hash_md5 = hashlib.md5()
            with open(model_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()

        raise ValueError("")

    @staticmethod
    def shorten_filename(file_stem: str) -> str:
        """
        model.get_compiled_path() fails if the model name is too long (activation=True super long)
        """
        max_length = 30
        return file_stem[:max_length] + "_SHORTENED"

    @staticmethod
    def from_path(
        model_path: Path,
        temp_dir: Optional[Path] = None,
        should_compile: bool = False,
        should_load: bool = True,
        compute_units: ct.ComputeUnit = ct.ComputeUnit.ALL,
        upload_id: Optional[str] = None,
        make_state: Optional[bool] = False, # for stateful models
    ) -> Optional["CoreMLModel"]:
        model_type: Optional[UploadedModelType] = None
        if model_path.suffix == ".mlpackage":
            model_type = UploadedModelType.MLPACKAGE
        elif model_path.suffix == ".mlmodelc":
            model_type = UploadedModelType.MLMODELC
        elif model_path.suffix == ".mlmodel":
            model_type = UploadedModelType.MLMODEL

        if model_type is not None and model_path is not None:
            return CoreMLModel(
                model_path,
                model_type=model_type,
                temp_dir=temp_dir,
                should_compile=should_compile,
                should_load=should_load,
                compute_units=compute_units,
                upload_id=upload_id,
                make_state=make_state
            )

    @staticmethod
    def compute_unit_from_string(compute_unit_str: str) -> ct.ComputeUnit:
        if compute_unit_str == "ALL":
            return ct.ComputeUnit.ALL
        elif compute_unit_str == "CPU_AND_GPU":
            return ct.ComputeUnit.CPU_AND_GPU
        elif compute_unit_str == "CPU_ONLY":
            return ct.ComputeUnit.CPU_ONLY
        elif compute_unit_str == "CPU_AND_NE":
            return ct.ComputeUnit.CPU_AND_NE
        else:
            raise ValueError(f"Unknown compute unit: {compute_unit_str}")

    @staticmethod
    def compute_unit_to_string(compute_unit: ct.ComputeUnit) -> str:
        if compute_unit == ct.ComputeUnit.ALL:
            return "ALL"
        elif compute_unit == ct.ComputeUnit.CPU_AND_GPU:
            return "CPU_AND_GPU"
        elif compute_unit == ct.ComputeUnit.CPU_ONLY:
            return "CPU_ONLY"
        elif compute_unit == ct.ComputeUnit.CPU_AND_NE:
            return "CPU_AND_NE"
        else:
            raise ValueError(f"Unknown compute unit: {compute_unit}")

    def prepare_inputs(self, torch_inputs: List[torch.Tensor|PIL.Image.Image|int], model_input_keys: list[str]) -> Dict[str, np.ndarray]:
        """
        Convert list of tensors to numpy float32 dict
        Not doing this inside execute() because that function will be benchmarked
        model_input_keys should be decided by the pipeline, because the ordering matters...
        i.e. the if you do get_input_keys() you may get a different ordering
        """

        numpy_inputs = []
        for input_tensor in torch_inputs:
            if isinstance(input_tensor, torch.Tensor):
                input = input_tensor.cpu().detach().numpy().astype(np.float32)
            elif isinstance(input_tensor, PIL.Image.Image):
                input = input_tensor
            elif isinstance(input_tensor, int):
                input = np.array([input_tensor], dtype=np.float32)
            else:
                raise ValueError(f"Input type {type(input_tensor)} not supported")
            numpy_inputs.append(input)

        # input_keys = self.get_input_keys()
        input_keys = model_input_keys
        input_dict = dict(zip(input_keys, numpy_inputs))
        return input_dict

    def prepare_outputs(self, model_output: Dict, model_output_keys: list[str]) -> List[torch.Tensor]:
        """
        Convert model output to list of torch tensors
        Not doing this inside execute() because that function will be benchmarked
        CoreML output is a numpy dict - this is the "model_output" parameter
        """
        torch_outputs = [
            torch.from_numpy(model_output[key]) for key in model_output_keys
        ]
        return torch_outputs

    @staticmethod
    def get_minimum_deployment_version(model_path: Path) -> CoreMLAvailability:
        spec = ct.utils.load_spec(str(model_path))
        return get_availability_mapping(spec.specificationVersion)

    def get_weights_array_dict(self) -> Dict[str, np.ndarray]:
        weight_metadata = cto.get_weights_metadata(self.model, weight_threshold=0)
        weights_dict = {}
        for name, metadata in weight_metadata.items():
            weights_dict[name] = metadata.val
        return weights_dict

    @staticmethod
    def rename_feature(
        model: ct.models.MLModel,
        old_name: Optional[str],
        new_name: str,
        rename_inputs: bool,
        rename_outputs: bool # False to ignore outputs
    ) -> ct.models.MLModel:
        """
        Rename a feature in the model, return a new model
        if old_name is None, then will rename all inputs or outputs, as long as only 1 input/output
        """
        if rename_inputs and rename_outputs:
            raise ValueError("Cannot rename both inputs and outputs")
        if old_name is None:
            if rename_inputs:
                assert len(model.get_spec().description.input) == 1, "Only 1 input allowed if old_name is None"
                old_name = model.get_spec().description.input[0].name
            elif rename_outputs:
                assert len(model.get_spec().description.output) == 1, "Only 1 output allowed if old_name is None"
                old_name = model.get_spec().description.output[0].name
        spec = model.get_spec()
        ct.utils.rename_feature(spec, old_name, new_name, rename_inputs=rename_inputs, rename_outputs=rename_outputs) # inplace rename spec
        new_input_names = [inp.name for inp in spec.description.input]
        new_output_names = [out.name for out in spec.description.output]
        if rename_inputs and new_name not in new_input_names:
            raise ValueError(f"New name '{new_name}' not in input names: {new_input_names}")
        if rename_outputs and new_name not in new_output_names:
            raise ValueError(f"New name '{new_name}' not in output names: {new_output_names}")
        converted_model = ct.models.MLModel(spec, weights_dir=model.weights_dir)
        return converted_model

    @staticmethod
    def sanitize_tf_tensor_name(name: str, remove_index_suffix:bool=True) -> str:
        """
        Sanitize the TF tensor name to be compatible with CoreML
        Eg. `Decoder/upsampling_merged:0` -> `Decoder_sampling_merged`
        remove_index_suffix, if true, will remove the ':0' suffix, because CoreML will remove it, but only if 1 input/output!
        """
        chars_to_replace = ["/", ":", "."]
        if remove_index_suffix:
            if name.endswith(":0") or name.endswith(":1") or name.endswith(":2"): # todo: fix this shit
                name = name[:-2]
        for char in chars_to_replace:
            name = name.replace(char, "_")
        return name
