"""Advanced table extraction from PDF using img2table with GPU support."""

from pathlib import Path
from typing import Any
import csv
import json
import os

from prism_docs.core import BasePDFOperation, register_operation


def _get_device() -> str:
    """Detect available device for torch (CUDA, MPS, or CPU)."""
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def _extract_tables_img2table(
    pdf_path: Path,
    pages: list[int] | None = None,
    ocr_lang: str = "eng",
    implicit_rows: bool = True,
    borderless_tables: bool = True,
    min_confidence: int = 50,
) -> list[dict]:
    """
    Extract tables using img2table library with optional OCR.

    Args:
        pdf_path: Path to the PDF file
        pages: List of page numbers to process (1-indexed), None for all
        ocr_lang: OCR language for text extraction
        implicit_rows: Detect implicit rows in tables
        borderless_tables: Detect tables without borders
        min_confidence: Minimum confidence for table detection

    Returns:
        List of dictionaries containing table data
    """
    from img2table.document import PDF
    from img2table.ocr import TesseractOCR

    # Initialize OCR engine
    ocr = TesseractOCR(n_threads=os.cpu_count() or 1, lang=ocr_lang)

    # Initialize PDF document
    doc = PDF(src=str(pdf_path))

    # Convert 1-indexed pages to 0-indexed if specified
    page_indices = None
    if pages:
        page_indices = [p - 1 for p in pages]

    # Extract tables with OCR
    extracted = doc.extract_tables(
        ocr=ocr,
        implicit_rows=implicit_rows,
        borderless_tables=borderless_tables,
        min_confidence=min_confidence,
    )

    all_tables = []

    for page_idx, tables in extracted.items():
        # Skip pages not in our list
        if page_indices is not None and page_idx not in page_indices:
            continue

        page_num = page_idx + 1  # Convert back to 1-indexed

        for table_idx, table in enumerate(tables):
            # Get the table as a pandas DataFrame
            df = table.df

            if df is None or df.empty:
                continue

            # Convert DataFrame to list of lists
            rows = []
            # Include header if exists
            if df.columns is not None:
                header = [str(col) for col in df.columns.tolist()]
                # Only add header if it's not just numeric indices
                if not all(
                    isinstance(c, int) or (isinstance(c, str) and c.isdigit()) for c in df.columns
                ):
                    rows.append(header)

            # Add data rows
            for _, row in df.iterrows():
                rows.append([str(cell) if cell is not None else "" for cell in row.tolist()])

            if rows:
                all_tables.append(
                    {
                        "page": page_num,
                        "table_num": table_idx + 1,
                        "rows": rows,
                        "bbox": {
                            "x1": table.bbox.x1,
                            "y1": table.bbox.y1,
                            "x2": table.bbox.x2,
                            "y2": table.bbox.y2,
                        },
                    }
                )

    return all_tables


@register_operation("ocr-table-v2")
class OCRTableV2Operation(BasePDFOperation):
    """Extract tables from PDF using img2table with GPU-accelerated detection."""

    @property
    def name(self) -> str:
        return "ocr-table-v2"

    @property
    def description(self) -> str:
        return "Extract tables from PDF using advanced detection (img2table)"

    @property
    def default_suffix(self) -> str:
        return "tables"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Extract tables from PDF using img2table.

        Args:
            input_path: Path to input PDF
            output_path: Path to output file
            lang: OCR language (default: eng)
            format: Output format: csv, tsv, json, xlsx (default: csv)
            pages: Specific pages to extract (default: all)
            implicit_rows: Detect implicit rows (default: True)
            borderless: Detect borderless tables (default: True)
            min_confidence: Minimum detection confidence 0-100 (default: 50)
        """
        lang = kwargs.get("lang", "eng")
        output_format = kwargs.get("format", "csv")
        pages = kwargs.get("pages")
        implicit_rows = kwargs.get("implicit_rows", True)
        borderless = kwargs.get("borderless", True)
        min_confidence = kwargs.get("min_confidence", 50)

        # Log device being used
        device = _get_device()
        if device == "cuda":
            import torch

            gpu_name = torch.cuda.get_device_name(0)
            print(f"Using GPU: {gpu_name}")
        elif device == "mps":
            print("Using Apple Silicon GPU (MPS)")
        else:
            print("Using CPU (no GPU detected)")

        # Extract tables
        all_tables = _extract_tables_img2table(
            input_path,
            pages=pages,
            ocr_lang=lang,
            implicit_rows=implicit_rows,
            borderless_tables=borderless,
            min_confidence=min_confidence,
        )

        # Handle empty results
        if not all_tables:
            if output_format == "json":
                output_path = output_path.with_suffix(".json")
                output_path.write_text(
                    json.dumps(
                        {"message": "No tables detected in document", "tables": []},
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            elif output_format == "xlsx":
                output_path = output_path.with_suffix(".xlsx")
                import pandas as pd

                pd.DataFrame({"Note": ["No tables detected in document"]}).to_excel(
                    output_path, index=False
                )
            else:
                suffix = ".csv" if output_format == "csv" else ".tsv"
                output_path = output_path.with_suffix(suffix)
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    f.write("# No tables detected in document\n")
            return

        # Output based on format
        if output_format == "csv":
            output_path = output_path.with_suffix(".csv")
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for table in all_tables:
                    writer.writerow([f"# Page {table['page']}, Table {table['table_num']}"])
                    for row in table["rows"]:
                        writer.writerow(row)
                    writer.writerow([])

        elif output_format == "tsv":
            output_path = output_path.with_suffix(".tsv")
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="\t")
                for table in all_tables:
                    writer.writerow([f"# Page {table['page']}, Table {table['table_num']}"])
                    for row in table["rows"]:
                        writer.writerow(row)
                    writer.writerow([])

        elif output_format == "json":
            output_path = output_path.with_suffix(".json")
            output_path.write_text(
                json.dumps(all_tables, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

        elif output_format == "xlsx":
            output_path = output_path.with_suffix(".xlsx")
            import pandas as pd

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for table in all_tables:
                    sheet_name = f"Page{table['page']}_Table{table['table_num']}"
                    # Truncate sheet name to Excel's 31-char limit
                    sheet_name = sheet_name[:31]
                    df = pd.DataFrame(table["rows"])
                    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
