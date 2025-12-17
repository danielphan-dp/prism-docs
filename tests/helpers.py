from pathlib import Path

from pypdf import PdfWriter


def make_pdf(path: Path, pages: int = 1, metadata: dict | None = None) -> Path:
    """Create a simple PDF with blank pages and optional metadata."""
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=200, height=200)

    if metadata:
        writer.add_metadata(metadata)

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        writer.write(f)

    return path
