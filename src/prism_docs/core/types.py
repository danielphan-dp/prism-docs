"""Core types and protocols for PDF operations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class OutputNaming(str, Enum):
    """Strategy for naming output files."""

    SUFFIX = "suffix"  # Add suffix to input filename
    PREFIX = "prefix"  # Add prefix to input filename
    FIXED = "fixed"  # Use a fixed output name
    CUSTOM = "custom"  # Use custom pattern


class OverwritePolicy(str, Enum):
    """Policy for handling existing output files."""

    OVERWRITE = "overwrite"
    SKIP = "skip"
    RENAME = "rename"  # Add number suffix
    ERROR = "error"


@dataclass
class OutputConfig:
    """Configuration for output file handling."""

    naming: OutputNaming = OutputNaming.SUFFIX
    suffix: str = ""
    prefix: str = ""
    fixed_name: str = ""
    pattern: str = "{stem}{suffix}{ext}"  # For custom naming
    output_dir: Path | None = None  # None = same as input
    overwrite: OverwritePolicy = OverwritePolicy.OVERWRITE

    def resolve_output_path(self, input_path: Path, operation_suffix: str = "") -> Path:
        """Resolve the output path based on configuration."""
        stem = input_path.stem
        ext = input_path.suffix
        use_operation_suffix = self.overwrite not in {
            OverwritePolicy.SKIP,
            OverwritePolicy.ERROR,
        }

        if self.naming == OutputNaming.SUFFIX:
            suffix = self.suffix or (f"-{operation_suffix}" if operation_suffix and use_operation_suffix else "")
            name = f"{stem}{suffix}{ext}"
        elif self.naming == OutputNaming.PREFIX:
            prefix = self.prefix or (f"{operation_suffix}-" if operation_suffix and use_operation_suffix else "")
            name = f"{prefix}{stem}{ext}"
        elif self.naming == OutputNaming.FIXED:
            name = self.fixed_name or f"output{ext}"
        else:  # CUSTOM
            name = self.pattern.format(
                stem=stem,
                ext=ext,
                suffix=self.suffix,
                prefix=self.prefix,
                operation=operation_suffix if use_operation_suffix else "",
            )

        output_dir = self.output_dir or input_path.parent
        output_path = output_dir / name

        return self._handle_existing(output_path)

    def _handle_existing(self, path: Path) -> Path:
        """Handle existing files based on overwrite policy."""
        if not path.exists() or self.overwrite == OverwritePolicy.OVERWRITE:
            return path

        if self.overwrite == OverwritePolicy.ERROR:
            raise FileExistsError(f"Output file already exists: {path}")

        if self.overwrite == OverwritePolicy.SKIP:
            raise FileExistsError(f"Skipping existing file: {path}")

        # RENAME: add number suffix
        counter = 1
        stem = path.stem
        while path.exists():
            path = path.with_stem(f"{stem}_{counter}")
            counter += 1

        return path


@dataclass
class OperationResult:
    """Result of a PDF operation."""

    success: bool
    input_path: Path
    output_path: Path | None = None
    message: str = ""
    error: Exception | None = None


@runtime_checkable
class PDFOperation(Protocol):
    """Protocol for PDF operations."""

    @property
    def name(self) -> str:
        """Operation name for CLI and logging."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description."""
        ...

    @property
    def default_suffix(self) -> str:
        """Default suffix for output files."""
        ...

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Execute the operation."""
        ...


class BasePDFOperation(ABC):
    """Base class for PDF operations with common functionality."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Operation name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description."""
        ...

    @property
    @abstractmethod
    def default_suffix(self) -> str:
        """Default suffix for output files."""
        ...

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Execute the operation with error handling."""
        input_path = Path(input_path)

        try:
            # Check if output_path was explicitly provided in kwargs
            explicit_output = kwargs.pop("output_path", None)
            if explicit_output:
                output_path = Path(explicit_output)
            else:
                output_path = output_config.resolve_output_path(input_path, self.default_suffix)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            self._execute(input_path, output_path, **kwargs)

            return OperationResult(
                success=True,
                input_path=input_path,
                output_path=output_path,
                message=f"Successfully processed '{input_path}' -> '{output_path}'",
            )

        except FileExistsError as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=str(e),
                error=e,
            )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Failed to process '{input_path}': {e}",
                error=e,
            )

    @abstractmethod
    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Internal execution logic. Override in subclasses."""
        ...


@dataclass
class OperationConfig:
    """Configuration for a specific operation."""

    enabled: bool = True
    output: OutputConfig = field(default_factory=OutputConfig)
    options: dict[str, Any] = field(default_factory=dict)
