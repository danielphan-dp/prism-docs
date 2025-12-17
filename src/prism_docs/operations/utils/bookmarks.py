"""Manage PDF bookmarks (outlines/table of contents)."""

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter

from prism_docs.core import BasePDFOperation, OperationResult, OutputConfig, register_operation


@register_operation("bookmarks")
class BookmarksOperation(BasePDFOperation):
    """View, add, or extract PDF bookmarks."""

    @property
    def name(self) -> str:
        return "bookmarks"

    @property
    def description(self) -> str:
        return "View, add, or extract PDF bookmarks (table of contents)"

    @property
    def default_suffix(self) -> str:
        return "bookmarked"

    def execute(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Handle bookmark operations."""
        input_path = Path(input_path)
        action: str = kwargs.get("action", "view")

        try:
            if action == "view":
                return self._view_bookmarks(input_path, **kwargs)
            elif action == "extract":
                return self._extract_bookmarks(input_path, output_config, **kwargs)
            elif action == "add":
                return self._add_bookmarks(input_path, output_config, **kwargs)
            else:
                return OperationResult(
                    success=False,
                    input_path=input_path,
                    message=f"Unknown action: {action}",
                )

        except Exception as e:
            return OperationResult(
                success=False,
                input_path=input_path,
                message=f"Bookmark operation failed: {e}",
                error=e,
            )

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """Not used - see execute override."""
        pass

    def _view_bookmarks(self, input_path: Path, **kwargs: Any) -> OperationResult:
        """View existing bookmarks."""
        reader = PdfReader(input_path)
        outline = reader.outline

        if not outline:
            return OperationResult(
                success=True,
                input_path=input_path,
                message=f"'{input_path}' has no bookmarks",
            )

        lines = [f"Bookmarks in '{input_path.name}':"]
        self._format_outline(outline, lines, indent=0)

        return OperationResult(
            success=True,
            input_path=input_path,
            message="\n".join(lines),
        )

    def _format_outline(self, outline: list, lines: list[str], indent: int) -> None:
        """Recursively format outline items."""
        for item in outline:
            if isinstance(item, list):
                # Nested bookmarks
                self._format_outline(item, lines, indent + 2)
            else:
                # Bookmark item
                prefix = " " * indent
                title = item.title if hasattr(item, "title") else str(item)
                lines.append(f"{prefix}- {title}")

    def _extract_bookmarks(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Extract bookmarks to a text file."""
        reader = PdfReader(input_path)
        outline = reader.outline

        if not outline:
            return OperationResult(
                success=True,
                input_path=input_path,
                message=f"'{input_path}' has no bookmarks to extract",
            )

        output_path = kwargs.get("output_path")
        if output_path is None:
            output_dir = output_config.output_dir or input_path.parent
            output_path = output_dir / f"{input_path.stem}_bookmarks.txt"
        else:
            output_path = Path(output_path)

        lines: list[str] = []
        self._extract_outline(outline, lines, level=0, reader=reader)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return OperationResult(
            success=True,
            input_path=input_path,
            output_path=output_path,
            message=f"Extracted bookmarks to '{output_path}'",
        )

    def _extract_outline(
        self,
        outline: list,
        lines: list[str],
        level: int,
        reader: PdfReader,
    ) -> None:
        """Recursively extract outline items with page numbers."""
        for item in outline:
            if isinstance(item, list):
                self._extract_outline(item, lines, level + 1, reader)
            else:
                title = item.title if hasattr(item, "title") else str(item)
                # Try to get page number
                page_num = ""
                try:
                    if hasattr(item, "page"):
                        page_idx = reader.get_destination_page_number(item)
                        if page_idx is not None:
                            page_num = f" (page {page_idx + 1})"
                except Exception:
                    pass

                indent = "  " * level
                lines.append(f"{indent}{title}{page_num}")

    def _add_bookmarks(
        self,
        input_path: Path,
        output_config: OutputConfig,
        **kwargs: Any,
    ) -> OperationResult:
        """Add bookmarks to a PDF."""
        bookmarks: list[dict] = kwargs.get("bookmarks", [])
        from_file: str | None = kwargs.get("from_file")

        if from_file:
            bookmarks = self._load_bookmarks_from_file(Path(from_file))

        if not bookmarks:
            return OperationResult(
                success=False,
                input_path=input_path,
                message="No bookmarks provided",
            )

        output_path = kwargs.get("output_path")
        if output_path is None:
            output_path = output_config.resolve_output_path(input_path, self.default_suffix)
        else:
            output_path = Path(output_path)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Add bookmarks
        for bookmark in bookmarks:
            title = bookmark.get("title", "Bookmark")
            page = bookmark.get("page", 1) - 1  # Convert to 0-indexed

            if 0 <= page < len(writer.pages):
                writer.add_outline_item(title, page)

        with open(output_path, "wb") as f:
            writer.write(f)

        return OperationResult(
            success=True,
            input_path=input_path,
            output_path=output_path,
            message=f"Added {len(bookmarks)} bookmarks to '{output_path}'",
        )

    def _load_bookmarks_from_file(self, path: Path) -> list[dict]:
        """Load bookmarks from a text file (format: title|page)."""
        bookmarks = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "|" in line:
                    title, page = line.rsplit("|", 1)
                    bookmarks.append({"title": title.strip(), "page": int(page.strip())})

        return bookmarks
