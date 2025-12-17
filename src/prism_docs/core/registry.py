"""Operation registry and plugin system."""

from collections.abc import Callable
from typing import Type

from prism_docs.core.types import BasePDFOperation


class OperationRegistry:
    """Registry for PDF operations with plugin support."""

    _instance: "OperationRegistry | None" = None
    _operations: dict[str, Type[BasePDFOperation]]

    def __new__(cls) -> "OperationRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._operations = {}
        return cls._instance

    def register(
        self, name: str | None = None
    ) -> Callable[[Type[BasePDFOperation]], Type[BasePDFOperation]]:
        """Decorator to register an operation."""

        def decorator(cls: Type[BasePDFOperation]) -> Type[BasePDFOperation]:
            op_name = name or cls.name.fget(cls)  # type: ignore
            self._operations[op_name] = cls
            return cls

        return decorator

    def get(self, name: str) -> Type[BasePDFOperation] | None:
        """Get an operation by name."""
        return self._operations.get(name)

    def get_instance(self, name: str) -> BasePDFOperation | None:
        """Get an instance of an operation by name."""
        op_class = self.get(name)
        if op_class:
            return op_class()
        return None

    def list_operations(self) -> list[str]:
        """List all registered operation names."""
        return list(self._operations.keys())

    def all(self) -> dict[str, Type[BasePDFOperation]]:
        """Get all registered operations."""
        return self._operations.copy()

    def clear(self) -> None:
        """Clear all registered operations (mainly for testing)."""
        self._operations.clear()


# Global registry instance
registry = OperationRegistry()


def register_operation(
    name: str | None = None,
) -> Callable[[Type[BasePDFOperation]], Type[BasePDFOperation]]:
    """Decorator to register an operation with the global registry."""
    return registry.register(name)
