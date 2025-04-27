from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import numpy as np
import torch

from runlocal_tools.dtypes.upload import UploadedModelType


def convert_numpy_dict_to_torch(input_dict: Dict[str, np.ndarray]) -> Dict[str, torch.Tensor]:
    return {k: torch.from_numpy(v) for k, v in input_dict.items()}

def convert_torch_dict_to_numpy(
    output_dict: Dict[str, torch.Tensor],
    np_type: Optional[np.dtype] = None
) -> Dict[str, np.ndarray]:
    """
    np_type can be passed in to cast the values to a specific numpy type
    needed because CoreML uses float32 inputs and outputs
    """
    if np_type is None:
        return {k: v.cpu().detach().numpy() for k, v in output_dict.items()}
    else:
        return {k: v.cpu().detach().numpy().astype(np_type) for k, v in output_dict.items()}


class Model(ABC):
    model_path: Optional[Path] = None
    model_type: UploadedModelType

    def __init__(self): ...

    def __enter__(self) -> "Model":
        return self

    @classmethod
    def get_model_type(cls) -> UploadedModelType:
        return cls.model_type

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass

    @abstractmethod
    def is_compiled(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def calculate_hash(*args, **kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_path(*args, **kwargs) -> Optional["Model"]:
        pass

    @abstractmethod
    def get_input_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_output_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_input_shape(self, index: int = 0) -> List[int]:
        pass

    @abstractmethod
    def get_output_shape(self, index: int = 0) -> List[int]:
        pass

    @abstractmethod
    def load_model(self, compile: bool = False, force: bool = False) -> None:
        pass

    @abstractmethod
    def load_compiled_model(self, force: bool = False) -> None:
        pass

    @abstractmethod
    def execute(self, model_input: Any, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def prepare_inputs(self, torch_inputs: List[torch.Tensor], model_input_keys: list[str]) -> Any:
        """
        because MLModel is generic even for torchscript models, we need to
        convert the torch inputs to the correct format for the on-device model framework
        which usually uses numpy arrays.
        For TorchScript models, this is a no-op.
        """
        pass

    @abstractmethod
    def prepare_outputs(self, model_output: Any, model_output_keys: list[str]) -> List[torch.Tensor]:
        """
        because MLModel is generic even for torchscript models, we need to
        convert the model outputs back to torch tensors
        For TorchScript models, this is a no-op.
        """
        pass

    def get_weights_array_dict(self) -> Dict[str, np.ndarray]:
        raise NotImplementedError
