import os
import numpy as np
from pathlib import Path
import aidge_core
from aidge_core.export_utils import ExportNode, ExportNodeCpp, generate_file
from aidge_export_cpp.utils import ROOT
from aidge_export_cpp import ExportLibCpp

##############################################
############## Export functions ##############
##############################################
def numpy_dtype2ctype(dtype):
    if dtype == np.int8:
        return "int8_t"
    elif dtype == np.int16:
        return "int16_t"
    elif dtype == np.int32:
        return "int32_t"
    elif dtype == np.int64:
        return "int64_t"
    elif dtype == np.float32:
        return "float"
    elif dtype == np.float64:
        return "double"
    # Add more dtype mappings as needed
    else:
        raise ValueError(f"Unsupported {dtype} dtype")

def export_params(name: str,
                  array: np.ndarray,
                  filepath: str):

    # Get directory name of the file
    dirname = os.path.dirname(filepath)

    # If directory doesn't exist, create it
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    generate_file(
        filepath,
        str(ROOT / "templates" / "data" / "parameters.jinja"),
        name=name,
        data_t=numpy_dtype2ctype(array.dtype),
        values=array.tolist()
    )


##############################################
############## Operators helper ##############
##############################################

@ExportLibCpp.register("Producer", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class ProducerCPP(ExportNode):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.values = np.array(self.operator.get_output(0))

        if len(self.values.shape) == 4:  # Note: export in HWC
            self.values =  np.transpose(self.values, (0, 2, 3, 1))

    def export(self, export_folder: Path):
        header_path = f"include/parameters/{self.attributes['name']}.h"
        export_params(
            self.attributes['out_name'][0],
            self.values.reshape(-1),
            str(export_folder / header_path))
        return [header_path]

    def forward(self):
        # A Producer does nothing during forward
        return []

# TODO : find a way to remove this dummy exportnode
@ExportLibCpp.register("Pad2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class PadCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["padding"] = node.get_operator().attr.begin_end_borders
        self.attributes["border_type"] = node.get_operator().attr.border_type
        self.attributes["border_value"] = node.get_operator().attr.border_value

        assert self.attributes["border_type"] == aidge_core.pad_border_type.Constant, (
            f"export Pad2d: border_type == {node.get_operator().attr.border_type} not implemented"
        )

        self.config_template = str(
            ROOT / "templates" / "configuration" / "pad_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "pad_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "pad.hpp")
        ]

@ExportLibCpp.register("ReLU", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ReLUCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Rectifier"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "activation_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "activation_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Reshape", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ReshapeCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.config_template = str(
            ROOT / "templates" / "configuration" / "reshape_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "reshape_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "reshape.hpp"),
        ]

@ExportLibCpp.register("MatMul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MatMulCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "matmul_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "matmul_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "matmul.hpp"),
        ]

def _setup_conv2D(conv):
    """Common setup code for convolutions: Conv2D and PaddedConv2D."""

    # If biases are not provided we set it as nullptr instead of None
    if (len(conv.attributes["in_name"]) > 2 and conv.attributes["in_name"][2] is None):
        conv.attributes["in_name"][2] = "nullptr"

    conv.attributes["activation"] = "Linear"
    conv.attributes["rescaling"] = "NoScaling"
    conv.config_template = str(
        ROOT / "templates" / "configuration" / "convolution_config.jinja")
    conv.forward_template = str(
        ROOT / "templates" / "kernel_forward" / "convolution_forward.jinja")
    conv.include_list = []
    conv.kernels_to_copy = [
        str(ROOT / "kernels" / "convolution.hpp"),
        str(ROOT / "kernels" / "macs.hpp"),
        str(ROOT / "kernels" / "activation.hpp"),
        str(ROOT / "kernels" / "rescaling.hpp")
    ]

@ExportLibCpp.register("Conv2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class ConvCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        # No padding with Conv
        # Use PaddedConv to add padding attribute
        self.attributes["padding"] = [0, 0]

        _setup_conv2D(self)

@ExportLibCpp.register_metaop("PaddedConv2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class PaddedConvCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        # TODO find a way to retrive attr for meta op
        for n in self.operator.get_micro_graph().get_nodes():
            if n.type() == "Pad2D":
                self.attributes["padding"] = n.get_operator(
                ).attr.begin_end_borders
            if n.type() == "Conv2D":
                self.attributes["kernel_dims"] = n.get_operator(
                ).attr.kernel_dims
                self.attributes["stride_dims"] = n.get_operator(
                ).attr.stride_dims
                self.attributes["dilation_dims"] = n.get_operator(
                ).attr.dilation_dims

        _setup_conv2D(self)

def _setup_elemwise_op(elemwise, op):
    """Common code (template and kernel setup) shared across all the different elementWise operator (Add, Sub,...)."""

    elemwise.attributes["elemwise_op"] = op
    elemwise.attributes["activation"] = "Linear"
    elemwise.attributes["rescaling"] = "NoScaling"
    elemwise.config_template = str(
        ROOT / "templates" / "configuration" / "elemwise_config.jinja")
    elemwise.forward_template = str(
        ROOT / "templates" / "kernel_forward" / "elemwise_forward.jinja")
    elemwise.include_list = []
    elemwise.kernels_to_copy = [
        str(ROOT / "kernels" / "elemwise.hpp"),
        str(ROOT / "kernels" / "activation.hpp"),
        str(ROOT / "kernels" / "rescaling.hpp")
    ]

@ExportLibCpp.register("Add", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class AddCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        _setup_elemwise_op(self, "Add")

@ExportLibCpp.register("Sub", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class SubCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        _setup_elemwise_op(self, "Sub")

@ExportLibCpp.register("Mul", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MulCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        _setup_elemwise_op(self, "Mul")

def _setup_pooling(pooling):
    """Common code (template and kernel setup) shared across all the different pooling operator."""

    pooling.config_template = str(
        ROOT / "templates" / "configuration" / "pooling_config.jinja")
    pooling.forward_template = str(
        ROOT / "templates" / "kernel_forward" / "pooling_forward.jinja")
    pooling.include_list = []
    pooling.kernels_to_copy = [
        str(ROOT / "kernels" / "pooling.hpp"),
        str(ROOT / "kernels" / "activation.hpp"),
        str(ROOT / "kernels" / "rescaling.hpp")
    ]

@ExportLibCpp.register("MaxPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class MaxPoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # No padding with MaxPooling
        # Use PaddedMaxPooling to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["pool_type"] = "Max"
        self.attributes["activation"] = "Linear"

        _setup_pooling(self)

@ExportLibCpp.register("AvgPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class AvgPoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        # No padding with MaxPooling
        # Use PaddedMaxPooling to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["pool_type"] = "Average"
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"

        _setup_pooling(self)

@ExportLibCpp.register_metaop("PaddedMaxPooling2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class PaddedMaxPoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        for n in self.operator.get_micro_graph().get_nodes():
            if n.type() == "Pad2D":
                self.attributes["padding"] = n.get_operator(
                ).attr.begin_end_borders
            if n.type() == "MaxPooling2D":
                self.attributes["kernel_dims"] = n.get_operator(
                ).attr.kernel_dims
                self.attributes["stride_dims"] = n.get_operator(
                ).attr.stride_dims
        self.attributes["pool_type"] = "Max"
        self.attributes["activation"] = "Linear"

        _setup_pooling(self)

@ExportLibCpp.register("GlobalAveragePooling", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class GlobalAveragePoolCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)

        self.attributes["stride_dims"] = [1, 1]
        # No padding with MaxPooling
        # Use PaddedMaxPooling to add padding attribute
        self.attributes["padding"] = [0, 0]
        self.attributes["kernel_dims"] = [
            self.attributes["in_height"][0],
            self.attributes["in_width"][0],
        ]
        self.attributes["pool_type"] = "Average"
        self.attributes["activation"] = "Linear"

        _setup_pooling(self)

@ExportLibCpp.register("FC", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class FcCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.config_template = str(
            ROOT / "templates" / "configuration" / "fullyconnected_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "fullyconnected_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "fullyconnected.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Transpose", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.any)))
class TransposeCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.config_template = str(
            ROOT / "templates" / "configuration" / "transpose_ND_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "transpose_ND_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "transpose.hpp")
        ]

@ExportLibCpp.register("Softmax", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class SoftmaxCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        assert self.node.get_nb_inputs() == 1, (
            f"export softmax: nb_inputs == {self.node.get_nb_inputs()} not implemented"
        )

        tensor = self.operator.get_input(0)
        nbDims = len(tensor.dims())
        axis = node.get_operator().attr.axis if node.get_operator().attr.axis >= 0 else node.get_operator().attr.axis + nbDims

        assert axis < nbDims, (
            f"export softmax: attribute axis == {node.get_operator().attr.axis} should be less than {nbDims}"
        )

        postAxisElems = 1
        for i in range(axis + 1, nbDims):
            postAxisElems *= tensor.dims()[i]

        preAxisElems = 1
        for i in range(axis):
            preAxisElems *= tensor.dims()[i]

        self.attributes["axis_size"] = tensor.dims()[axis]
        self.attributes["axis_size_post"] = postAxisElems
        self.attributes["axis_size_pre"] = preAxisElems

        self.config_template = str(
            ROOT / "templates" / "configuration" / "softmax_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "softmax_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "softmax.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
        ]

@ExportLibCpp.register("BatchNorm2D", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class BatchNorm2DCPP(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.attributes["activation"] = "Linear"
        self.attributes["rescaling"] = "NoScaling"
        self.attributes["epsilon"] = node.get_operator().attr.epsilon
        self.config_template = str(
            ROOT / "templates" / "configuration" / "batchnorm_config.jinja")
        self.forward_template = str(
            ROOT / "templates" / "kernel_forward" / "batchnorm_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "batchnorm.hpp"),
            str(ROOT / "kernels" / "macs.hpp"),
            str(ROOT / "kernels" / "activation.hpp"),
            str(ROOT / "kernels" / "rescaling.hpp")
        ]

@ExportLibCpp.register("Concat", aidge_core.ImplSpec(aidge_core.IOSpec(aidge_core.dtype.float32)))
class Concat(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        assert self.node.get_nb_inputs() >= 1, (
            f"export softmax: nb_inputs == {self.node.get_nb_inputs()} not implemented"
        )

        inputIndex = 0

        tensor = self.operator.get_input(0)
        for idx, _ in enumerate(self.node.inputs()):
            if self.operator.get_input(idx) is not None:
                tensor = self.operator.get_input(idx)
                nbDims = len(tensor.dims())
                axis = node.get_operator().attr.axis if node.get_operator().attr.axis >= 0 else node.get_operator().attr.axis + nbDims

                assert axis < nbDims, (
                    f"export softmax: attribute axis == {axis} should be less than {nbDims}"
                )

                postAxisElems = 1
                for i in range(axis + 1, nbDims):
                    postAxisElems *= tensor.dims()[i]

                preAxisElems = 1
                for i in range(axis):
                    preAxisElems *= tensor.dims()[i]

                if (inputIndex == 0):
                    self.attributes["axis_size_post"] = postAxisElems
                    self.attributes["axis_size_pre"] = preAxisElems

                    self.attributes["axis_size"] = [None] * self.attributes["nb_in"]
                else:
                    assert self.attributes["axis_size_post"] == postAxisElems, (
                        f"export concat: axis_size_post {self.attributes['axis_size_post']} != {postAxisElems}"
                    )
                    assert self.attributes["axis_size_pre"] == preAxisElems, (
                        f"export concat: axis_size_pre {self.attributes['axis_size_pre']} != {preAxisElems}"
                    )

                self.attributes["axis_size"][idx] = tensor.dims()[axis]
            else:
                assert false, (
                    f"export concat: input {idx} is None, not implemented")

            inputIndex += 1

        self.config_template = str(ROOT / "templates" / "configuration" / "concat_config.jinja")
        self.forward_template = str(ROOT / "templates" / "kernel_forward" / "concat_forward.jinja")
        self.include_list = []
        self.kernels_to_copy = [
            str(ROOT / "kernels" / "concat.hpp"),
        ]