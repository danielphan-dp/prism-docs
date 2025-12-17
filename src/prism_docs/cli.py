"""Command-line interface for Prism Docs."""

import argparse
import sys
from pathlib import Path
from typing import Any

# Import operations to register them
import prism_docs.operations  # noqa: F401
from prism_docs.core import Config, load_config
from prism_docs.core.runner import PDFRunner


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="prism-docs",
        description="CLI toolkit for PDF editing, security, OCR, and image conversion.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global options
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Path to configuration file (YAML)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress output",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without doing it",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Process multiple files in parallel",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for output files",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Original operations
    _add_encrypt_command(subparsers)
    _add_decrypt_command(subparsers)
    _add_merge_command(subparsers)
    _add_watermark_command(subparsers)
    _add_compress_command(subparsers)
    _add_extract_pages_command(subparsers)
    _add_extract_text_command(subparsers)
    _add_rotate_command(subparsers)
    _add_split_command(subparsers)
    _add_metadata_command(subparsers)

    # Page manipulation operations
    _add_page_numbers_command(subparsers)
    _add_stamp_command(subparsers)
    _add_reverse_command(subparsers)
    _add_interleave_command(subparsers)
    _add_remove_pages_command(subparsers)
    _add_overlay_command(subparsers)

    # Image operations
    _add_images_to_pdf_command(subparsers)
    _add_pdf_to_images_command(subparsers)
    _add_extract_images_command(subparsers)

    # Security operations
    _add_flatten_command(subparsers)
    _add_permissions_command(subparsers)
    _add_redact_command(subparsers)

    # Info and utility operations
    _add_info_command(subparsers)
    _add_validate_command(subparsers)
    _add_crop_command(subparsers)
    _add_resize_command(subparsers)
    _add_bookmarks_command(subparsers)

    # OCR operations
    _add_ocr_command(subparsers)
    _add_ocr_extract_command(subparsers)
    _add_searchable_pdf_command(subparsers)
    _add_ocr_batch_command(subparsers)
    _add_ocr_data_command(subparsers)
    _add_ocr_table_command(subparsers)
    _add_ocr_table_v2_command(subparsers)
    _add_ocr_detect_lang_command(subparsers)
    _add_ocr_multi_lang_command(subparsers)

    # Config management commands
    _add_config_command(subparsers)
    _add_list_command(subparsers)

    return parser


def _add_encrypt_command(subparsers) -> None:
    parser = subparsers.add_parser("encrypt", help="Encrypt a PDF with a password")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("password", help="Password to encrypt the PDF")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument("--owner-password", help="Owner password (defaults to user password)")
    parser.add_argument(
        "--algorithm",
        choices=["RC4-40", "RC4-128", "AES-128", "AES-256"],
        default="AES-256",
        help="Encryption algorithm",
    )


def _add_decrypt_command(subparsers) -> None:
    parser = subparsers.add_parser("decrypt", help="Decrypt a password-protected PDF")
    parser.add_argument("input", type=Path, help="Encrypted PDF file")
    parser.add_argument("password", help="Password to decrypt the PDF")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")


def _add_merge_command(subparsers) -> None:
    parser = subparsers.add_parser("merge", help="Merge multiple PDF files into one")
    parser.add_argument("output", type=Path, help="Output PDF file")
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF files to merge")


def _add_watermark_command(subparsers) -> None:
    parser = subparsers.add_parser("watermark", help="Add a watermark to all pages")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("watermark", type=Path, help="Watermark PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--layer",
        choices=["above", "below"],
        default="below",
        help="Place watermark above or below content",
    )
    parser.add_argument(
        "--pages",
        type=str,
        help="Pages to watermark (e.g., '1,3,5' or '1-5')",
    )


def _add_compress_command(subparsers) -> None:
    parser = subparsers.add_parser("compress", help="Lossless compress PDF files")
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF files to compress")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file (single input only)")


def _add_extract_pages_command(subparsers) -> None:
    parser = subparsers.add_parser("extract-pages", help="Extract pages from a PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument("--start", type=int, default=1, help="Start page (1-indexed)")
    parser.add_argument("--end", type=int, help="End page (1-indexed, inclusive)")
    parser.add_argument(
        "--pages",
        type=str,
        help="Specific pages to extract (e.g., '1,3,5' or '1-5,8')",
    )


def _add_extract_text_command(subparsers) -> None:
    parser = subparsers.add_parser("extract-text", help="Extract text from PDF files")
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF files to extract text from")
    parser.add_argument("-o", "--output", type=Path, help="Output text file (single input only)")
    parser.add_argument(
        "--separator",
        default="\n\n",
        help="Separator between pages (default: blank line)",
    )


def _add_rotate_command(subparsers) -> None:
    parser = subparsers.add_parser("rotate", help="Rotate pages in a PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument(
        "degrees",
        type=int,
        choices=[90, 180, 270],
        help="Rotation degrees (clockwise)",
    )
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--pages",
        type=str,
        help="Pages to rotate (e.g., '1,3,5' or '1-5')",
    )


def _add_split_command(subparsers) -> None:
    parser = subparsers.add_parser("split", help="Split a PDF into multiple files")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument(
        "--mode",
        choices=["pages", "ranges"],
        default="pages",
        help="Split mode: individual pages or by ranges",
    )
    parser.add_argument(
        "--ranges",
        type=str,
        help="Page ranges for 'ranges' mode (e.g., '1-3,4-6,7-10')",
    )
    parser.add_argument("--output-dir", type=Path, help="Output directory")


def _add_metadata_command(subparsers) -> None:
    parser = subparsers.add_parser("metadata", help="View or edit PDF metadata")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument(
        "--action",
        choices=["view", "edit"],
        default="view",
        help="Action to perform",
    )
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file (for edit)")
    parser.add_argument("--title", help="Set document title")
    parser.add_argument("--author", help="Set document author")
    parser.add_argument("--subject", help="Set document subject")


# Page manipulation commands
def _add_page_numbers_command(subparsers) -> None:
    parser = subparsers.add_parser("page-numbers", help="Add page numbers to PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--position",
        choices=[
            "bottom-center",
            "bottom-left",
            "bottom-right",
            "top-center",
            "top-left",
            "top-right",
        ],
        default="bottom-center",
        help="Position of page numbers",
    )
    parser.add_argument(
        "--format", default="Page {n} of {total}", help="Format string for page numbers"
    )
    parser.add_argument("--font-size", type=float, default=12, help="Font size in points")
    parser.add_argument("--margin", type=float, default=36, help="Margin from edge in points")
    parser.add_argument("--start", type=int, default=1, help="Starting page number")
    parser.add_argument("--skip-first", action="store_true", help="Skip numbering on first page")


def _add_stamp_command(subparsers) -> None:
    parser = subparsers.add_parser("stamp", help="Add text stamp to PDF pages")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("text", help="Text to stamp")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--position",
        choices=["center", "top-left", "top-right", "bottom-left", "bottom-right"],
        default="center",
        help="Position of stamp",
    )
    parser.add_argument("--font-size", type=float, default=48, help="Font size in points")
    parser.add_argument("--rotation", type=float, default=45, help="Rotation angle in degrees")
    parser.add_argument("--opacity", type=float, default=0.3, help="Stamp opacity (0-1)")
    parser.add_argument("--color", default="gray", help="Stamp color (red, gray, blue)")
    parser.add_argument("--pages", type=str, help="Pages to stamp (e.g., '1,3,5' or '1-5')")


def _add_reverse_command(subparsers) -> None:
    parser = subparsers.add_parser("reverse", help="Reverse page order in PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")


def _add_interleave_command(subparsers) -> None:
    parser = subparsers.add_parser("interleave", help="Interleave pages from two PDFs")
    parser.add_argument("input1", type=Path, help="First PDF file (odd pages)")
    parser.add_argument("input2", type=Path, help="Second PDF file (even pages)")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--reverse-second", action="store_true", help="Reverse second PDF's page order"
    )


def _add_remove_pages_command(subparsers) -> None:
    parser = subparsers.add_parser("remove-pages", help="Remove pages from PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("pages", type=str, help="Pages to remove (e.g., '1,3,5' or '2-4')")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")


def _add_overlay_command(subparsers) -> None:
    parser = subparsers.add_parser("overlay", help="Overlay one PDF on top of another")
    parser.add_argument("input", type=Path, help="Base PDF file")
    parser.add_argument("overlay", type=Path, help="Overlay PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument("--pages", type=str, help="Pages to overlay (e.g., '1,3,5' or '1-5')")


# Image operation commands
def _add_images_to_pdf_command(subparsers) -> None:
    parser = subparsers.add_parser("images-to-pdf", help="Convert images to PDF")
    parser.add_argument("images", nargs="+", type=Path, help="Image files to convert")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PDF file")
    parser.add_argument("--page-size", default="A4", help="Page size (A4, Letter, etc.)")
    parser.add_argument("--margin", type=float, default=36, help="Margin in points")
    parser.add_argument(
        "--fit", choices=["contain", "cover", "stretch"], default="contain", help="Fit mode"
    )


def _add_pdf_to_images_command(subparsers) -> None:
    parser = subparsers.add_parser("pdf-to-images", help="Convert PDF pages to images")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("--output-dir", type=Path, help="Output directory for images")
    parser.add_argument(
        "--format", choices=["png", "jpeg", "webp"], default="png", help="Image format"
    )
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution (DPI)")
    parser.add_argument("--pages", type=str, help="Pages to convert (e.g., '1,3,5' or '1-5')")


def _add_extract_images_command(subparsers) -> None:
    parser = subparsers.add_parser("extract-images", help="Extract embedded images from PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("--output-dir", type=Path, help="Output directory for images")
    parser.add_argument(
        "--format", choices=["original", "png", "jpeg"], default="original", help="Output format"
    )
    parser.add_argument("--min-size", type=int, default=0, help="Minimum image dimension in pixels")


# Security operation commands
def _add_flatten_command(subparsers) -> None:
    parser = subparsers.add_parser("flatten", help="Flatten PDF annotations and forms")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--annotations", action="store_true", default=True, help="Flatten annotations"
    )
    parser.add_argument("--forms", action="store_true", default=True, help="Flatten form fields")


def _add_permissions_command(subparsers) -> None:
    parser = subparsers.add_parser("permissions", help="Set PDF permissions")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("--owner-password", required=True, help="Owner password")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument("--allow-print", action="store_true", help="Allow printing")
    parser.add_argument("--allow-copy", action="store_true", help="Allow copying content")
    parser.add_argument("--allow-modify", action="store_true", help="Allow modifications")
    parser.add_argument("--allow-annotate", action="store_true", help="Allow annotations")
    parser.add_argument("--allow-forms", action="store_true", help="Allow form filling")


def _add_redact_command(subparsers) -> None:
    parser = subparsers.add_parser("redact", help="Redact regions from PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--regions", type=str, help="Regions to redact (format: page:x1,y1,x2,y2;...)"
    )
    parser.add_argument("--text", type=str, help="Text pattern to redact (regex)")
    parser.add_argument("--color", default="black", help="Redaction color")


# Info and utility commands
def _add_info_command(subparsers) -> None:
    parser = subparsers.add_parser("info", help="Show PDF information")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed metadata")
    parser.add_argument("--json", action="store_true", help="Output as JSON")


def _add_validate_command(subparsers) -> None:
    parser = subparsers.add_parser("validate", help="Validate PDF file integrity")
    parser.add_argument("inputs", nargs="+", type=Path, help="PDF files to validate")
    parser.add_argument("--strict", action="store_true", help="Use strict validation mode")


def _add_crop_command(subparsers) -> None:
    parser = subparsers.add_parser("crop", help="Crop PDF page margins")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument("--left", type=float, default=0, help="Left margin to crop (points)")
    parser.add_argument("--right", type=float, default=0, help="Right margin to crop (points)")
    parser.add_argument("--top", type=float, default=0, help="Top margin to crop (points)")
    parser.add_argument("--bottom", type=float, default=0, help="Bottom margin to crop (points)")
    parser.add_argument("--margin", type=float, help="Uniform margin to crop (points)")
    parser.add_argument("--percent", type=float, help="Percentage of page to crop from each edge")
    parser.add_argument("--pages", type=str, help="Pages to crop (e.g., '1,3,5' or '1-5')")


def _add_resize_command(subparsers) -> None:
    parser = subparsers.add_parser("resize", help="Resize PDF pages")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output PDF file")
    parser.add_argument(
        "--size", choices=["A4", "A3", "A5", "Letter", "Legal", "Tabloid"], help="Target paper size"
    )
    parser.add_argument("--width", type=float, help="Target width in points")
    parser.add_argument("--height", type=float, help="Target height in points")
    parser.add_argument("--scale", type=float, help="Scale factor (e.g., 0.5 for half size)")
    parser.add_argument(
        "--fit", choices=["contain", "cover", "stretch"], default="contain", help="Fit mode"
    )
    parser.add_argument("--pages", type=str, help="Pages to resize (e.g., '1,3,5' or '1-5')")


def _add_bookmarks_command(subparsers) -> None:
    parser = subparsers.add_parser("bookmarks", help="Manage PDF bookmarks")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument(
        "--action",
        choices=["view", "extract", "add"],
        default="view",
        help="Action to perform",
    )
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    parser.add_argument(
        "--from-file", type=Path, help="File with bookmarks to add (format: title|page)"
    )


# OCR operation commands
def _add_ocr_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr", help="Extract text from scanned PDF using OCR")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output text file")
    parser.add_argument("--lang", default="eng", help="OCR language (default: eng)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion (default: 300)")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode (default: 3)")
    parser.add_argument("--oem", type=int, default=3, help="OCR engine mode (default: 3)")
    parser.add_argument("--pages", type=str, help="Pages to OCR (e.g., '1-5' or '1,3,5')")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per page in seconds")


def _add_ocr_extract_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-extract", help="OCR with image preprocessing")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode")
    parser.add_argument(
        "--preprocess", choices=["none", "threshold", "blur", "sharpen", "denoise"], default="none"
    )
    parser.add_argument("--threshold", type=int, default=128, help="Binarization threshold (0-255)")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contrast factor")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness factor")
    parser.add_argument("--invert", action="store_true", help="Invert colors")
    parser.add_argument("--format", choices=["text", "hocr", "tsv", "box", "data"], default="text")


def _add_searchable_pdf_command(subparsers) -> None:
    parser = subparsers.add_parser(
        "searchable-pdf", help="Create searchable PDF with OCR text layer"
    )
    parser.add_argument("input", type=Path, help="Input scanned PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output searchable PDF file")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per page in seconds")


def _add_ocr_batch_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-batch", help="Batch OCR multiple PDFs")
    parser.add_argument("inputs", nargs="+", type=Path, help="Input PDF files")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode")
    parser.add_argument("--output-type", choices=["txt", "pdf"], default="txt", help="Output type")
    parser.add_argument("--fast", action="store_true", help="Fast mode with lower DPI")


def _add_ocr_data_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-data", help="Extract OCR data with bounding boxes")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON file")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode")
    parser.add_argument("--min-confidence", type=int, default=0, help="Minimum confidence (0-100)")
    parser.add_argument("--level", choices=["word", "line", "block", "page"], default="word")


def _add_ocr_table_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-table", help="Extract tables from scanned PDF")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--format", choices=["csv", "tsv", "json"], default="csv")
    parser.add_argument("--pages", type=str, help="Pages to extract (e.g., '1-5')")


def _add_ocr_table_v2_command(subparsers) -> None:
    parser = subparsers.add_parser(
        "ocr-table-v2", help="Extract tables using advanced detection (GPU-accelerated)"
    )
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output file")
    parser.add_argument("--lang", default="eng", help="OCR language")
    parser.add_argument(
        "--format", choices=["csv", "tsv", "json", "xlsx"], default="csv", help="Output format"
    )
    parser.add_argument("--pages", type=str, help="Pages to extract (e.g., '1-5' or '1,3,5')")
    parser.add_argument(
        "--implicit-rows", action="store_true", default=True, help="Detect implicit rows"
    )
    parser.add_argument(
        "--no-implicit-rows",
        action="store_false",
        dest="implicit_rows",
        help="Disable implicit row detection",
    )
    parser.add_argument(
        "--borderless", action="store_true", default=True, help="Detect borderless tables"
    )
    parser.add_argument(
        "--no-borderless",
        action="store_false",
        dest="borderless",
        help="Only detect bordered tables",
    )
    parser.add_argument("--min-confidence", type=int, default=50, help="Minimum confidence (0-100)")


def _add_ocr_detect_lang_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-detect-lang", help="Auto-detect language and OCR")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output text file")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--fallback-lang", default="eng", help="Fallback language")
    parser.add_argument("--sample-pages", type=int, default=1, help="Pages to sample for detection")


def _add_ocr_multi_lang_command(subparsers) -> None:
    parser = subparsers.add_parser("ocr-multi-lang", help="OCR with multiple languages")
    parser.add_argument("input", type=Path, help="Input PDF file")
    parser.add_argument("-o", "--output", type=Path, help="Output text file")
    parser.add_argument("--langs", default="eng+fra+deu", help="Languages (+-separated)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion")
    parser.add_argument("--psm", type=int, default=3, help="Page segmentation mode")


def _add_config_command(subparsers) -> None:
    parser = subparsers.add_parser("config", help="Manage configuration")
    parser.add_argument(
        "action",
        choices=["show", "init", "path"],
        help="Config action",
    )


def _add_list_command(subparsers) -> None:
    subparsers.add_parser("list", help="List available operations")


def parse_page_spec(spec: str) -> list[int]:
    """Parse a page specification like '1,3,5-8' into a list of page numbers."""
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def parse_ranges(spec: str) -> list[tuple[int, int]]:
    """Parse a range specification like '1-3,4-6' into a list of tuples."""
    ranges = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ranges.append((int(start), int(end)))
        else:
            n = int(part)
            ranges.append((n, n))
    return ranges


def _parse_redact_regions(spec: str) -> list[dict]:
    """Parse redact region specification like 'page:x1,y1,x2,y2;page:x1,y1,x2,y2'."""
    regions = []
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            page_part, coords = part.split(":", 1)
            page = int(page_part.strip())
            x1, y1, x2, y2 = map(float, coords.split(","))
            regions.append({"page": page, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
    return regions


def main() -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    # Load configuration
    config = load_config(args.config)

    # Apply CLI overrides
    if args.verbose:
        config.global_settings.verbose = True
    if args.quiet:
        config.global_settings.quiet = True
    if args.dry_run:
        config.global_settings.dry_run = True
    if args.parallel:
        config.global_settings.parallel = True
    if hasattr(args, "output_dir") and args.output_dir:
        config.default_output.output_dir = args.output_dir

    # Create runner
    runner = PDFRunner(config)

    try:
        return _execute_command(args, runner, config)
    except Exception as e:
        if not config.global_settings.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return 1


def _execute_command(args, runner: PDFRunner, config: Config) -> int:
    """Execute the requested command."""
    quiet = config.global_settings.quiet

    if args.command == "list":
        print("Available operations:")
        for name, desc in runner.list_operations():
            print(f"  {name}: {desc}")
        return 0

    if args.command == "config":
        return _handle_config_command(args, config)

    # Build kwargs from args
    kwargs: dict[str, Any] = {}

    if args.command == "encrypt":
        kwargs["password"] = args.password
        if args.owner_password:
            kwargs["owner_password"] = args.owner_password
        kwargs["algorithm"] = args.algorithm
        results = runner.run("encrypt", args.input, args.output, **kwargs)

    elif args.command == "decrypt":
        kwargs["password"] = args.password
        results = runner.run("decrypt", args.input, args.output, **kwargs)

    elif args.command == "merge":
        kwargs["merge_inputs"] = [Path(p) for p in args.inputs]
        kwargs["output_path"] = args.output
        results = runner.run("merge", args.inputs[0], **kwargs)

    elif args.command == "watermark":
        kwargs["watermark_path"] = args.watermark
        kwargs["layer"] = args.layer
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("watermark", args.input, args.output, **kwargs)

    elif args.command == "compress":
        results = runner.run("compress", args.inputs, args.output, **kwargs)

    elif args.command == "extract-pages":
        kwargs["start"] = args.start
        if args.end:
            kwargs["end"] = args.end
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("extract-pages", args.input, args.output, **kwargs)

    elif args.command == "extract-text":
        kwargs["separator"] = args.separator
        results = runner.run("extract-text", args.inputs, args.output, **kwargs)

    elif args.command == "rotate":
        kwargs["degrees"] = args.degrees
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("rotate", args.input, args.output, **kwargs)

    elif args.command == "split":
        kwargs["mode"] = args.mode
        if args.ranges:
            kwargs["ranges"] = parse_ranges(args.ranges)
        if args.output_dir:
            config.default_output.output_dir = args.output_dir
        results = runner.run("split", args.input, **kwargs)

    elif args.command == "metadata":
        kwargs["action"] = args.action
        if args.title:
            kwargs["title"] = args.title
        if args.author:
            kwargs["author"] = args.author
        if args.subject:
            kwargs["subject"] = args.subject
        results = runner.run("metadata", args.input, args.output, **kwargs)

    # Page manipulation commands
    elif args.command == "page-numbers":
        kwargs["position"] = args.position
        kwargs["format"] = args.format
        kwargs["font_size"] = args.font_size
        kwargs["margin"] = args.margin
        kwargs["start_number"] = args.start
        kwargs["skip_first"] = args.skip_first
        results = runner.run("page-numbers", args.input, args.output, **kwargs)

    elif args.command == "stamp":
        kwargs["text"] = args.text
        kwargs["position"] = args.position
        kwargs["font_size"] = args.font_size
        kwargs["rotation"] = args.rotation
        kwargs["opacity"] = args.opacity
        kwargs["color"] = args.color
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("stamp", args.input, args.output, **kwargs)

    elif args.command == "reverse":
        results = runner.run("reverse", args.input, args.output, **kwargs)

    elif args.command == "interleave":
        kwargs["second_path"] = args.input2
        kwargs["reverse_second"] = args.reverse_second
        results = runner.run("interleave", args.input1, args.output, **kwargs)

    elif args.command == "remove-pages":
        kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("remove-pages", args.input, args.output, **kwargs)

    elif args.command == "overlay":
        kwargs["overlay_path"] = args.overlay
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("overlay", args.input, args.output, **kwargs)

    # Image operation commands
    elif args.command == "images-to-pdf":
        kwargs["image_paths"] = args.images
        kwargs["page_size"] = args.page_size
        kwargs["margin"] = args.margin
        kwargs["fit"] = args.fit
        kwargs["output_path"] = args.output
        results = runner.run("images-to-pdf", args.images[0], **kwargs)

    elif args.command == "pdf-to-images":
        kwargs["format"] = args.format
        kwargs["dpi"] = args.dpi
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        if args.output_dir:
            config.default_output.output_dir = args.output_dir
        results = runner.run("pdf-to-images", args.input, **kwargs)

    elif args.command == "extract-images":
        kwargs["format"] = args.format
        kwargs["min_size"] = args.min_size
        if args.output_dir:
            config.default_output.output_dir = args.output_dir
        results = runner.run("extract-images", args.input, **kwargs)

    # Security operation commands
    elif args.command == "flatten":
        kwargs["annotations"] = args.annotations
        kwargs["forms"] = args.forms
        results = runner.run("flatten", args.input, args.output, **kwargs)

    elif args.command == "permissions":
        kwargs["owner_password"] = args.owner_password
        kwargs["print"] = args.allow_print
        kwargs["copy"] = args.allow_copy
        kwargs["modify"] = args.allow_modify
        kwargs["annotations"] = args.allow_annotate
        kwargs["forms"] = args.allow_forms
        results = runner.run("permissions", args.input, args.output, **kwargs)

    elif args.command == "redact":
        if args.regions:
            kwargs["regions"] = _parse_redact_regions(args.regions)
        if args.text:
            kwargs["text_pattern"] = args.text
        color_name = (args.color or "black").lower()
        color_map = {
            "black": (0, 0, 0),
            "white": (1, 1, 1),
            "red": (1, 0, 0),
            "green": (0, 1, 0),
            "blue": (0, 0, 1),
            "gray": (0.5, 0.5, 0.5),
        }
        kwargs["color"] = color_map.get(color_name, (0, 0, 0))
        results = runner.run("redact", args.input, args.output, **kwargs)

    # Info and utility commands
    elif args.command == "info":
        kwargs["verbose"] = getattr(args, "verbose", False)
        kwargs["json"] = args.json
        results = runner.run("info", args.input, **kwargs)

    elif args.command == "validate":
        kwargs["strict"] = args.strict
        results = runner.run("validate", args.inputs, **kwargs)

    elif args.command == "crop":
        kwargs["left"] = args.left
        kwargs["right"] = args.right
        kwargs["top"] = args.top
        kwargs["bottom"] = args.bottom
        if args.margin is not None:
            kwargs["margin"] = args.margin
        if args.percent is not None:
            kwargs["percent"] = args.percent
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("crop", args.input, args.output, **kwargs)

    elif args.command == "resize":
        if args.size:
            kwargs["size"] = args.size
        if args.width:
            kwargs["width"] = args.width
        if args.height:
            kwargs["height"] = args.height
        if args.scale:
            kwargs["scale"] = args.scale
        kwargs["fit"] = args.fit
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("resize", args.input, args.output, **kwargs)

    elif args.command == "bookmarks":
        kwargs["action"] = args.action
        if args.from_file:
            kwargs["from_file"] = str(args.from_file)
        if args.output:
            kwargs["output_path"] = args.output
        results = runner.run("bookmarks", args.input, **kwargs)

    # OCR commands
    elif args.command == "ocr":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        kwargs["oem"] = args.oem
        kwargs["timeout"] = args.timeout
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("ocr", args.input, args.output, **kwargs)

    elif args.command == "searchable-pdf":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        kwargs["timeout"] = args.timeout
        results = runner.run("searchable-pdf", args.input, args.output, **kwargs)

    elif args.command == "ocr-extract":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        kwargs["preprocess"] = args.preprocess
        kwargs["threshold"] = args.threshold
        kwargs["contrast"] = args.contrast
        kwargs["brightness"] = args.brightness
        kwargs["invert"] = args.invert
        kwargs["format"] = args.format
        results = runner.run("ocr-extract", args.input, args.output, **kwargs)

    elif args.command == "ocr-batch":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        kwargs["output_type"] = args.output_type
        kwargs["fast"] = args.fast
        if args.output_dir:
            config.default_output.output_dir = args.output_dir
        results = runner.run("ocr-batch", args.inputs, **kwargs)

    elif args.command == "ocr-data":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        kwargs["min_confidence"] = args.min_confidence
        kwargs["level"] = args.level
        results = runner.run("ocr-data", args.input, args.output, **kwargs)

    elif args.command == "ocr-detect-lang":
        kwargs["dpi"] = args.dpi
        kwargs["fallback_lang"] = args.fallback_lang
        kwargs["sample_pages"] = args.sample_pages
        results = runner.run("ocr-detect-lang", args.input, args.output, **kwargs)

    elif args.command == "ocr-multi-lang":
        kwargs["langs"] = args.langs
        kwargs["dpi"] = args.dpi
        kwargs["psm"] = args.psm
        results = runner.run("ocr-multi-lang", args.input, args.output, **kwargs)

    elif args.command == "ocr-table":
        kwargs["lang"] = args.lang
        kwargs["dpi"] = args.dpi
        kwargs["format"] = args.format
        if args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("ocr-table", args.input, args.output, **kwargs)

    elif args.command == "ocr-table-v2":
        kwargs["lang"] = args.lang
        kwargs["format"] = args.format
        kwargs["implicit_rows"] = args.implicit_rows
        kwargs["borderless"] = args.borderless
        kwargs["min_confidence"] = args.min_confidence
        if hasattr(args, "pages") and args.pages:
            kwargs["pages"] = parse_page_spec(args.pages)
        results = runner.run("ocr-table-v2", args.input, args.output, **kwargs)

    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    # Print results
    if not quiet:
        for result in results:
            print(result.message)

    # Return 0 if all succeeded, 1 otherwise
    return 0 if all(r.success for r in results) else 1


def _handle_config_command(args, config: Config) -> int:
    """Handle config subcommand."""
    from prism_docs.core.config import get_default_config_path

    if args.action == "path":
        print(get_default_config_path())

    elif args.action == "show":
        import yaml  # type: ignore[import-untyped]

        print(yaml.dump(config.to_dict(), default_flow_style=False))

    elif args.action == "init":
        path = get_default_config_path()
        if path.exists():
            print(f"Config already exists at: {path}")
            return 1
        config.to_yaml(path)
        print(f"Created config at: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
