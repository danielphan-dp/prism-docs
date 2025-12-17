# Python API

## Quick Start

```python
from prism_docs import run_operation

# Simple operations
run_operation("encrypt", "input.pdf", password="secret")
run_operation("compress", "large.pdf")
run_operation("rotate", "input.pdf", degrees=90)
```

## With Configuration

```python
from prism_docs import PDFRunner, Config

config = Config.from_yaml("config.yaml")
runner = PDFRunner(config)

results = runner.run("compress", ["file1.pdf", "file2.pdf"])

for result in results:
    if result.success:
        print(f"Output: {result.output_path}")
    else:
        print(f"Error: {result.message}")
```

## Operation Results

```python
@dataclass
class OperationResult:
    success: bool
    input_path: Path
    output_path: Path | None
    message: str
    error: Exception | None
```

## Custom Operations

```python
from prism_docs import BasePDFOperation, register_operation
from pathlib import Path

@register_operation("my-operation")
class MyOperation(BasePDFOperation):
    @property
    def name(self) -> str:
        return "my-operation"

    @property
    def description(self) -> str:
        return "My custom PDF operation"

    @property
    def default_suffix(self) -> str:
        return "processed"

    def _execute(self, input_path: Path, output_path: Path, **kwargs) -> None:
        # Implementation
        pass
```

## Available Operations

```python
from prism_docs import PDFRunner, Config

runner = PDFRunner(Config())
for name, description in runner.list_operations():
    print(name, description)
```

## Operation Parameters

### encrypt

```python
run_operation("encrypt", "input.pdf",
    password="secret",
    algorithm="AES-256"
)
```

### decrypt

```python
run_operation("decrypt", "input.pdf", password="secret")
```

### merge

```python
run_operation("merge", "first.pdf",
    output_path="merged.pdf",
    merge_inputs=["first.pdf", "second.pdf", "third.pdf"]
)
```

### watermark

```python
run_operation("watermark", "input.pdf",
    watermark_path="watermark.pdf",
    layer="below"  # below, above
)
```

### extract-pages

```python
run_operation("extract-pages", "input.pdf",
    start=1,
    end=5
)
# or
run_operation("extract-pages", "input.pdf",
    pages="1,3,5-8"
)
```

### rotate

```python
run_operation("rotate", "input.pdf",
    degrees=90,  # 90, 180, 270
    pages="1,3,5"  # optional, default: all
)
```

### split

```python
run_operation("split", "input.pdf",
    mode="pages",  # pages, ranges
    output_dir="./output"
)
# or
run_operation("split", "input.pdf",
    mode="ranges",
    ranges="1-3,4-6,7-10"
)
```

### permissions

```python
run_operation("permissions", "input.pdf",
    owner_password="admin",
    user_password="user",  # optional
    allow_print=True,
    allow_copy=True,
    allow_modify=False,
    allow_annotate=False
)
```
