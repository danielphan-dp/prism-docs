"""PDF operation runner with configuration support."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from prism_docs.core import (
    Config,
    OperationResult,
    OutputConfig,
    registry,
)


class PDFRunner:
    """Runner for executing PDF operations with configuration."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()

    def run(
        self,
        operation_name: str,
        input_paths: list[Path] | Path,
        output_path: Path | None = None,
        **kwargs,
    ) -> list[OperationResult]:
        """
        Run an operation on one or more input files.

        Args:
            operation_name: Name of the registered operation.
            input_paths: Single path or list of input paths.
            output_path: Optional output path (for single-file operations).
            **kwargs: Operation-specific arguments.

        Returns:
            List of OperationResult objects.
        """
        # Normalize input paths
        if isinstance(input_paths, (str, Path)):
            input_paths = [Path(input_paths)]
        else:
            input_paths = [Path(p) for p in input_paths]

        # Get operation
        operation = registry.get_instance(operation_name)
        if operation is None:
            raise ValueError(f"Unknown operation: {operation_name}")

        # Get operation config
        op_config = self.config.get_operation_config(operation_name)

        # Merge config options with kwargs (kwargs take precedence)
        merged_kwargs = {**op_config.options, **kwargs}

        # Handle output path
        output_config = op_config.output
        if output_path:
            merged_kwargs["output_path"] = output_path

        # Run operation(s)
        results = []

        if self.config.global_settings.parallel and len(input_paths) > 1:
            results = self._run_parallel(operation, input_paths, output_config, merged_kwargs)
        else:
            for input_path in input_paths:
                if self.config.global_settings.dry_run:
                    result = OperationResult(
                        success=True,
                        input_path=input_path,
                        message=f"[DRY RUN] Would process '{input_path}'",
                    )
                else:
                    result = operation.execute(input_path, output_config, **merged_kwargs)

                results.append(result)

                if self.config.global_settings.verbose and not self.config.global_settings.quiet:
                    print(result.message)

        return results

    def _run_parallel(
        self,
        operation,
        input_paths: list[Path],
        output_config: OutputConfig,
        kwargs: dict,
    ) -> list[OperationResult]:
        """Run operations in parallel."""
        results = []
        max_workers = self.config.global_settings.max_workers

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(operation.execute, path, output_config, **kwargs): path
                for path in input_paths
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

                if self.config.global_settings.verbose and not self.config.global_settings.quiet:
                    print(result.message)

        return results

    def list_operations(self) -> list[tuple[str, str]]:
        """List all available operations."""
        return [(name, op_class().description) for name, op_class in registry.all().items()]


def run_operation(
    operation_name: str,
    input_paths: list[Path] | Path,
    config: Config | None = None,
    **kwargs,
) -> list[OperationResult]:
    """Convenience function to run an operation."""
    runner = PDFRunner(config)
    return runner.run(operation_name, input_paths, **kwargs)
