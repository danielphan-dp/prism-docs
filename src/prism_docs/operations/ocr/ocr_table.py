"""Table extraction from PDF using OCR."""

import csv
import json
from pathlib import Path
from typing import Any

import pytesseract
from pdf2image import convert_from_path

from prism_docs.core import BasePDFOperation, register_operation


def _detect_table_regions(
    ocr_data: dict[str, list], img_width: int, min_columns: int = 2
) -> list[dict]:
    """
    Detect table-like regions by analyzing column alignment.

    Args:
        ocr_data: Tesseract OCR data dict
        img_width: Image width in pixels
        min_columns: Minimum columns to consider as table

    Returns:
        List of detected tables with rows
    """
    n_boxes = len(ocr_data["text"])
    if n_boxes == 0:
        return []

    # Group words by block and line
    blocks: dict[int, dict[int, list[dict]]] = {}
    for i in range(n_boxes):
        text = ocr_data["text"][i].strip()
        if not text:
            continue

        block_num = ocr_data["block_num"][i]
        line_num = ocr_data["line_num"][i]
        left = ocr_data["left"][i]
        width = ocr_data["width"][i]

        if block_num not in blocks:
            blocks[block_num] = {}
        if line_num not in blocks[block_num]:
            blocks[block_num][line_num] = []

        blocks[block_num][line_num].append(
            {"text": text, "left": left, "width": width, "right": left + width}
        )

    tables = []

    for block_num, lines in blocks.items():
        # Analyze if this block has table-like structure
        if len(lines) < 2:
            continue

        # Get all left positions across lines
        all_left_positions: list[int] = []
        for line_words in lines.values():
            all_left_positions.extend([w["left"] for w in line_words])

        if len(all_left_positions) < 4:
            continue

        # Cluster left positions to find columns
        sorted_positions = sorted(set(all_left_positions))
        column_clusters: list[list[int]] = []
        current_cluster: list[int] = [sorted_positions[0]]

        # Tolerance for column alignment (5% of image width)
        tolerance = img_width * 0.05

        for pos in sorted_positions[1:]:
            if pos - current_cluster[-1] < tolerance:
                current_cluster.append(pos)
            else:
                if len(current_cluster) >= 2:  # Column must appear in at least 2 lines
                    column_clusters.append(current_cluster)
                current_cluster = [pos]

        if len(current_cluster) >= 2:
            column_clusters.append(current_cluster)

        # Need at least min_columns aligned columns for a table
        if len(column_clusters) < min_columns:
            continue

        # Get column boundaries
        column_bounds = [(min(c), max(c)) for c in column_clusters]

        # Extract table rows
        table_rows = []
        for line_num in sorted(lines.keys()):
            line_words = sorted(lines[line_num], key=lambda w: w["left"])
            row: list[str] = [""] * len(column_bounds)

            for word in line_words:
                word_center = word["left"] + word["width"] // 2
                # Find which column this word belongs to
                for col_idx, (col_min, col_max) in enumerate(column_bounds):
                    # Word center is within column bounds (with tolerance)
                    if col_min - tolerance <= word_center <= col_max + tolerance * 3:
                        if row[col_idx]:
                            row[col_idx] += " " + word["text"]
                        else:
                            row[col_idx] = word["text"]
                        break
                else:
                    # Word doesn't fit in any column, append to nearest
                    min_dist = float("inf")
                    nearest_col = 0
                    for col_idx, (col_min, col_max) in enumerate(column_bounds):
                        dist = min(abs(word_center - col_min), abs(word_center - col_max))
                        if dist < min_dist:
                            min_dist = dist
                            nearest_col = col_idx
                    if row[nearest_col]:
                        row[nearest_col] += " " + word["text"]
                    else:
                        row[nearest_col] = word["text"]

            # Only add rows that have content in multiple columns
            non_empty_cols = sum(1 for cell in row if cell.strip())
            if non_empty_cols >= min_columns:
                table_rows.append(row)

        if len(table_rows) >= 2:  # Need at least 2 rows for a table
            tables.append({"block": block_num, "rows": table_rows})

    return tables


def _extract_all_text_as_table(ocr_data: dict[str, list]) -> list[list[str]]:
    """Fallback: extract all text organized by lines (not as table structure)."""
    n_boxes = len(ocr_data["text"])
    lines: dict[tuple[int, int], list[tuple[int, str]]] = {}

    for i in range(n_boxes):
        text = ocr_data["text"][i].strip()
        if not text:
            continue

        block_num = ocr_data["block_num"][i]
        line_num = ocr_data["line_num"][i]
        left = ocr_data["left"][i]
        key = (block_num, line_num)

        if key not in lines:
            lines[key] = []
        lines[key].append((left, text))

    # Sort by block then line, and reconstruct lines
    result = []
    for key in sorted(lines.keys()):
        words = sorted(lines[key], key=lambda x: x[0])
        line_text = " ".join(w[1] for w in words)
        result.append([line_text])

    return result


@register_operation("ocr-table")
class OCRTableOperation(BasePDFOperation):
    """Extract tables from PDF using OCR with intelligent table detection."""

    @property
    def name(self) -> str:
        return "ocr-table"

    @property
    def description(self) -> str:
        return "Extract tables from scanned PDF using OCR"

    @property
    def default_suffix(self) -> str:
        return "table"

    def _execute(self, input_path: Path, output_path: Path, **kwargs: Any) -> None:
        """
        Extract tables from PDF.

        Args:
            input_path: Path to input PDF
            output_path: Path to output file
            lang: OCR language (default: eng)
            dpi: DPI for conversion (default: 300)
            format: Output format: csv, tsv, json (default: csv)
            pages: Specific pages to extract (default: all)
            min_columns: Minimum columns to detect as table (default: 2)
        """
        lang = kwargs.get("lang", "eng")
        dpi = kwargs.get("dpi", 300)
        output_format = kwargs.get("format", "csv")
        pages = kwargs.get("pages")
        min_columns = kwargs.get("min_columns", 2)

        # PSM 3 for auto page segmentation, better for mixed content
        tess_config = "--psm 3 --oem 3"

        if pages:
            images = convert_from_path(
                input_path,
                dpi=dpi,
                first_page=pages[0],
                last_page=pages[-1],
            )
        else:
            images = convert_from_path(input_path, dpi=dpi)

        all_tables: list[dict] = []
        for page_num, image in enumerate(images, start=1):
            img_width = image.width

            # Get OCR data with position info
            ocr_data = pytesseract.image_to_data(
                image,
                lang=lang,
                config=tess_config,
                output_type=pytesseract.Output.DICT,
            )

            # Try to detect actual tables
            tables = _detect_table_regions(ocr_data, img_width, min_columns)

            if tables:
                for table_idx, table in enumerate(tables):
                    all_tables.append(
                        {
                            "page": page_num,
                            "table_num": table_idx + 1,
                            "rows": table["rows"],
                        }
                    )

        # Output based on format
        if not all_tables:
            # If no tables detected, create an empty output with a note
            if output_format == "json":
                output_path = output_path.with_suffix(".json")
                output_path.write_text(
                    json.dumps(
                        {"message": "No tables detected in document", "tables": []},
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            else:
                suffix = ".csv" if output_format == "csv" else ".tsv"
                output_path = output_path.with_suffix(suffix)
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    f.write("# No tables detected in document\n")
            return

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
                json.dumps(all_tables, indent=2, ensure_ascii=False), encoding="utf-8"
            )
