from enum import Enum


class UploadedModelType(str, Enum):
    MLPACKAGE = "MLPACKAGE"
    MLMODEL = "MLMODEL"
    MLMODELC = "MLMODELC"
    OPENVINO = "OPENVINO"
    ONNX = "ONNX"
    TF_SAVED_MODEL = "TF_SAVED_MODEL"
    EXECUTORCH = "EXECUTORCH"
    TORCHSCRIPT = "TORCHSCRIPT"

    # Keras can be saved in 3 different file formats
    KERAS_H5 = "KERAS_H5"
    KERAS_SAVED_MODEL = "KERAS_SAVED_MODEL"
    KERAS_KERAS = "KERAS_KERAS"

    TFLITE = "TFLITE"
    TFLITE_ZIPPED = "TFLITE_ZIPPED"

    # 'HF' means the config is understandable by HF transformers.
    # 'MLX'/'Torch' refers to the safetensor types
    HF_SAFETENSORS_PT = "HF_SAFETENSORS_PT"
    HF_SAFETENSORS_MLX = "HF_SAFETENSORS_MLX"

    PYTORCH = "PYTORCH"  # actual pytorch nn.Module

    GGUF = "GGUF"
    MNN = "MNN"
    NCNN = "NCNN"