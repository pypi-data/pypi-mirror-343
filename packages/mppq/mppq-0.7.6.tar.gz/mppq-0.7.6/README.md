# Minimal PPQ (mPPQ) PPQ 裁剪版

> PPQ [Readme](./README_PPQ.md)

This repo will continue the development of PPQ, maintain features and fix bugs.
I pruned most deprecated APIs and sample codes, functions in original PPQ and make it more extensible and easier to use.

## Key Changes

#### 1. TargetPlatform

`TargetPlatform` in PPQ mixed the concept of **Precision** and **Device**. We can see `TargetPlatform.OPENVINO_INT8` comes with `TargetPlatform.INT8`.

In mPPQ, I separate the concept of **Precision** and **Device** and all calls to `TargetPlatform` are now changed to `TargetPrecision`.

I also removed platforms support in PPQ because they are lacking of correct maintenance and support.
Instead of that, I add a new api to register your customized platform as well as your frontend parser, dispatcher and quantizer.

#### 2. Extension

Users need to register their own platforms to perform a correct quantization. There is no pre-defined platforms in mPPQ, just a sample quantizer for example.

Let me explain the way users need to follow.

1. [Parser](mppq/frontend/base.py#L14) and [Exporter](mppq/frontend/base.py#L15)

I keep `onnx_parser` and `onnxruntime_exporter` as the default graph serialization and de-serialization methods. Users can create a new parser by inheriting `GraphBuilder` and a new exporter by inheriting `GraphExporter`.

```python
class MyParser(GraphBuilder):
    def build(self, model_object: Any, **kwargs) -> BaseGraph:
        """Parser offers the way how to read from a model object and turn it into PPQ BaseGraph.
        """
        ...

class MyExporter(GraphExporter):
    def export(
        self,
        file_path: str | os.PathLike,
        graph: BaseGraph,
        config_path: Optional[str] = None,
        **kwargs,
    ):
        """Exporter offers the way how to serialize a PPQ BaseGraph into a model object.
        ...
```

The model object can be `onnx` or others like openvino `.xml` or qnn `.dlc`.


2. [Dispatcher](mppq/dispatcher/base.py#104)

Dispatcher is the core concept from PPQ, it will analysis the whole graph and decide which op should be quantized in which precision.

In mPPQ, all pre-defined dispatchers in PPQ are still kept, and they are:

- [allin](mppq/dispatcher/allin.py)
- [aggressive](mppq/dispatcher/aggressive.py)
- [conservative](mppq/dispatcher/conservative.py)
- [pointwise](mppq/dispatcher/pointwise.py)
- [perseus](mppq/dispatcher/perseus.py)

Users can create a new dispatcher by inheriting `GraphDispatcher` and implement its own logic.


3. [Quantizer](mppq/quantizer/base.py#L249)

Quantizer is a fundamental component in PPQ, it will control all the operations that needed to quantize a model.

In mPPQ quantizer, it will offer 3 abstract methods for users to implement:

```python
@abstractmethod
def init_quantize_config(self, operation: Operation) -> OperationQuantizationConfig:
    r"""Return a query to the operation how it should be quantized."""
    raise NotImplementedError

@property
def default_prequant_pipeline(self) -> QuantizationOptimizationPipeline:
    r"""A simplified API to return a default quantization pipeline."""
    return QuantizationOptimizationPipeline([])

@property
def default_quant_pipeline(self) -> QuantizationOptimizationPipeline:
    r"""A simplified API to return a default quantization pipeline."""
    raise NotImplementedError
```

Quantizer doesn't work with dispatcher any more, now user's dispatcher (or builtin ones) must dispatch all operations in the graph to a specific precision, if one of the operation is `Precision.UNSPECIFIED`, quantizer will raise an error now.

4. Platform

In mPPQ, I provide a register to support add new parsers, exporters, dispatchers and quantizers to a specific platform from external codebase.

```python
from mppq.api import load_quantizer, register_platform, export_ppq_graph

MyPlatformID = 1

register_platform(
    MyPlatformID,
    dispatcher={"mydisp": MyDispatcher},
    quantizer={"myquant": MyQuantizer},
    parsers={"myparser": MyParser},
    exporters={"myexporter": MyExporter},
)

quantizer = load_quantizer("mymodel.onnx", MyPlatformID)
quantized_graph = quantizer.quantize()
export_ppq_graph(quantized_graph, "quantized_mymodel.onnx")
```

Users can use builtin dispatcher by specifying a name in `load_quantizer`, but I highly recommend to know very detail of your platform and design your own dispatcher and quantizer.

```python
register_platform(
    MyPlatformID,
    dispatcher={},  # need to specify a builtin dispatcher name in quantize api
    quantizer={"myquant": MyQuantizer},
    parsers={},  # use builtin onnx parser
    exporters={},  # use builtin onnx exporter
)

quantizer = load_quantizer("mymodel.onnx", MyPlatformID, dispatcher="allin")
```


5. [Operation](mppq/executor/op/base.py#L135)

In mPPQ, most ONNX operators up to opset 19 are supported. In order to add a new support from users code base, users can register a new operation to a specific platform.

```python
from mppq.api import register_operation

@register_operation("myop", MyPlatformID)
def myop_forward(
    op: Operation,
    values: Sequence[torch.Tensor],
    ctx: Optional[TorchBackendContext] = None,
    **kwargs,
) -> torch.Tensor | Tuple[torch.Tensor, ...]:
    """
    Args:
        op: operation information (precision, attributes, types, etc.)
        values: input tensors
        ctx: execution device information

    Returns:
        a result tensor or a tuple of result tensors
    """
    ...
```


## Contribution

All mPPQ python codes are clean with flake8, black, and pyright (_except for mppq/executor/op/default.py_).

Test coverage: 51% (v0.7.1)

## Acknowledgement

[PPQ](https://github.com/OpenPPL/ppq)
