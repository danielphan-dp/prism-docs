from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import FileNotDecryptedError, PdfReadError


DEFAULT_PASSWORDS = ["", "owner", "secret", "password", "mypassword", "1234"]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TEXT_EXTS = {".txt", ".md", ".csv", ".tsv"}


def _norm_text(s: str) -> str:
    return s.replace("\r\n", "\n").strip() + "\n"


def _decrypt_if_possible(reader: PdfReader, passwords: list[str]) -> bool:
    if not reader.is_encrypted:
        return True
    for pw in passwords:
        try:
            ok = reader.decrypt(pw)
        except Exception:
            ok = 0
        if ok:
            return True
    return False


def _validate_demo_files(demo_dir: Path, *, passwords: list[str]) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    encrypted_unknown = 0
    checked = 0

    try:
        from PIL import Image  # type: ignore[import-untyped]
    except Exception:
        Image = None  # type: ignore[assignment]

    for path in sorted([p for p in demo_dir.rglob("*") if p.is_file()]):
        ext = path.suffix.lower()
        try:
            if ext == ".pdf":
                reader = PdfReader(path)
                decrypted = _decrypt_if_possible(reader, passwords)
                if reader.is_encrypted and not decrypted:
                    encrypted_unknown += 1
                    continue
                _ = len(reader.pages)
                checked += 1

            elif ext in IMAGE_EXTS:
                if Image is None:
                    continue
                with Image.open(path) as img:
                    img.verify()
                    if img.width <= 0 or img.height <= 0:
                        raise ValueError("invalid image dimensions")
                checked += 1

            elif ext == ".json":
                json.loads(path.read_text(encoding="utf-8"))
                checked += 1

            elif ext in TEXT_EXTS:
                if path.stat().st_size == 0:
                    raise ValueError("empty text file")
                checked += 1

        except (
            PdfReadError,
            FileNotDecryptedError,
            OSError,
            ValueError,
            json.JSONDecodeError,
        ) as e:
            errors.append(f"{path}: {type(e).__name__}: {e}")

    return checked, encrypted_unknown, errors


def _validate_demo_outputs_match_current_ops(
    demo_dir: Path, artifacts_dir: Path, *, passwords: list[str]
) -> tuple[int, list[str]]:
    import prism_docs.operations  # noqa: F401
    from prism_docs.core import Config
    from prism_docs.core.runner import PDFRunner

    runner = PDFRunner(Config())

    failures: list[str] = []
    checked = 0

    for dataset_dir in sorted([p for p in demo_dir.iterdir() if p.is_dir()]):
        dataset = dataset_dir.name
        input_pdf = artifacts_dir / f"{dataset}.pdf"
        if not input_pdf.exists():
            failures.append(f"missing input pdf for dataset {dataset}: {input_pdf}")
            continue

        # metadata
        metadata_path = dataset_dir / "metadata" / "metadata.txt"
        if metadata_path.exists():
            expected = runner.run("metadata", input_pdf, action="view")[0].message
            got = metadata_path.read_text(encoding="utf-8")
            checked += 1
            if _norm_text(expected) != _norm_text(got):
                failures.append(f"{metadata_path}: mismatch vs current 'metadata' output")

        # info
        info_path = dataset_dir / "info" / "info.txt"
        if info_path.exists():
            expected = runner.run("info", input_pdf)[0].message
            got = info_path.read_text(encoding="utf-8")
            checked += 1
            if _norm_text(expected) != _norm_text(got):
                failures.append(f"{info_path}: mismatch vs current 'info' output")

        # validate (both validate.txt and validation.txt)
        validate_dir = dataset_dir / "validate"
        for name in ["validate.txt", "validation.txt"]:
            vp = validate_dir / name
            if vp.exists():
                expected = runner.run("validate", input_pdf)[0].message
                got = vp.read_text(encoding="utf-8")
                checked += 1
                if _norm_text(expected) != _norm_text(got):
                    failures.append(f"{vp}: mismatch vs current 'validate' output")

        # extract-text
        extract_dir = dataset_dir / "extract-text"
        if extract_dir.exists():
            candidates = [extract_dir / f"{dataset}.txt", extract_dir / "text.txt"]
            target = next((p for p in candidates if p.exists()), None)
            if target is not None:
                with tempfile.TemporaryDirectory() as td:
                    out_path = Path(td) / "out.txt"
                    runner.run("extract-text", input_pdf, output_path=out_path)
                    expected = out_path.read_text(encoding="utf-8")
                got = target.read_text(encoding="utf-8")
                checked += 1
                if _norm_text(expected) != _norm_text(got):
                    failures.append(f"{target}: mismatch vs current 'extract-text' output")

        # bookmarks (demo may contain either view output or extracted bookmarks)
        bookmarks_path = dataset_dir / "bookmarks" / "bookmarks.txt"
        if bookmarks_path.exists():
            got = bookmarks_path.read_text(encoding="utf-8")
            if "(page " in got:
                with tempfile.TemporaryDirectory() as td:
                    out_path = Path(td) / "bookmarks.txt"
                    runner.run("bookmarks", input_pdf, action="extract", output_path=out_path)
                    if not out_path.exists():
                        failures.append(
                            f"{bookmarks_path}: demo looks like extract output, but current extract produced no file"
                        )
                    else:
                        expected = out_path.read_text(encoding="utf-8")
                        checked += 1
                        if _norm_text(expected) != _norm_text(got):
                            failures.append(
                                f"{bookmarks_path}: mismatch vs current 'bookmarks --action extract' output"
                            )
            else:
                expected = runner.run("bookmarks", input_pdf, action="view")[0].message
                checked += 1
                if _norm_text(expected) != _norm_text(got):
                    failures.append(
                        f"{bookmarks_path}: mismatch vs current 'bookmarks' view output"
                    )

    return checked, failures


def _validate_demo_semantics(
    demo_dir: Path, artifacts_dir: Path, *, passwords: list[str]
) -> list[str]:
    issues: list[str] = []

    A4 = (595.0, 842.0)

    def pdf_pages(path: Path, *, require_decrypt: bool = True) -> tuple[int, PdfReader, bool]:
        reader = PdfReader(path)
        decrypted = _decrypt_if_possible(reader, passwords)
        if require_decrypt and reader.is_encrypted and not decrypted:
            raise FileNotDecryptedError(f"Could not decrypt {path}")
        return len(reader.pages) if (decrypted or not reader.is_encrypted) else 0, reader, decrypted

    for dataset_dir in sorted([p for p in demo_dir.iterdir() if p.is_dir()]):
        dataset = dataset_dir.name
        input_pdf = artifacts_dir / f"{dataset}.pdf"
        if not input_pdf.exists():
            issues.append(f"{dataset}: missing input pdf {input_pdf}")
            continue

        in_pages, in_reader, _ = pdf_pages(input_pdf, require_decrypt=True)
        in_first = in_reader.pages[0]
        in_w = float(in_first.mediabox.width)
        in_h = float(in_first.mediabox.height)

        # split: expect one file per page
        split_dir = dataset_dir / "split"
        if split_dir.exists():
            split_files = sorted(split_dir.glob(f"{dataset}_page_*.pdf"))
            if split_files and len(split_files) != in_pages:
                issues.append(
                    f"{dataset}/split: expected {in_pages} files, found {len(split_files)}"
                )
            for f in split_files:
                n, _, _ = pdf_pages(f, require_decrypt=False)
                if n != 1:
                    issues.append(f"{f}: expected 1 page, found {n}")

        # remove-pages: without_page1.pdf should have one fewer page
        rp = dataset_dir / "remove-pages" / "without_page1.pdf"
        if rp.exists():
            n, _, _ = pdf_pages(rp, require_decrypt=False)
            if n != max(in_pages - 1, 0):
                issues.append(
                    f"{dataset}/remove-pages/without_page1.pdf: expected {in_pages - 1} pages, found {n}"
                )

        # extract-pages: infer count from filename
        ep_dir = dataset_dir / "extract-pages"
        if ep_dir.exists():
            for f in sorted(ep_dir.glob("*.pdf")):
                m = re.search(r"pages_?(\d+)-(\d+)", f.stem)
                if not m:
                    continue
                start, end = int(m.group(1)), int(m.group(2))
                expected = end - start + 1
                n, _, _ = pdf_pages(f, require_decrypt=False)
                if n != expected:
                    issues.append(f"{f}: expected {expected} pages from name, found {n}")

        # pdf-to-images: ensure page numbers are valid
        pti_dir = dataset_dir / "pdf-to-images"
        if pti_dir.exists():
            page_nums: list[int] = []
            for img in pti_dir.glob("*.png"):
                m = re.search(r"page_(\d+)$", img.stem)
                if m:
                    page_nums.append(int(m.group(1)))
            if page_nums:
                if any(p < 1 or p > in_pages for p in page_nums):
                    issues.append(
                        f"{dataset}/pdf-to-images: contains out-of-range page numbers (1..{in_pages})"
                    )
                if len(set(page_nums)) != len(page_nums):
                    issues.append(f"{dataset}/pdf-to-images: duplicate page numbers")

        # encrypt/decrypt
        enc = dataset_dir / "encrypt" / "encrypted.pdf"
        if enc.exists():
            reader = PdfReader(enc)
            if not reader.is_encrypted:
                issues.append(f"{enc}: expected encrypted PDF")

        dec = dataset_dir / "decrypt" / "decrypted.pdf"
        if dec.exists():
            reader = PdfReader(dec)
            if reader.is_encrypted:
                issues.append(f"{dec}: expected decrypted (not encrypted)")
            else:
                n, _, _ = pdf_pages(dec, require_decrypt=False)
                if n != in_pages:
                    issues.append(f"{dec}: expected {in_pages} pages, found {n}")

        # permissions: restricted.pdf should be encrypted but decryptable with empty user password
        perm = dataset_dir / "permissions" / "restricted.pdf"
        if perm.exists():
            reader = PdfReader(perm)
            if not reader.is_encrypted:
                issues.append(f"{perm}: expected encrypted permissions PDF")
            else:
                ok = 0
                try:
                    ok = reader.decrypt("")
                except Exception:
                    ok = 0
                if not ok:
                    issues.append(f"{perm}: expected decryptable with empty user password")

        # rotate: if filename includes rotated_<deg>, verify rotation
        rot_dir = dataset_dir / "rotate"
        if rot_dir.exists():
            for f in rot_dir.glob("*.pdf"):
                m = re.search(r"rotated_(\d+)$", f.stem)
                if not m:
                    continue
                deg = int(m.group(1)) % 360
                n, reader, decrypted = pdf_pages(f, require_decrypt=False)
                if not decrypted and reader.is_encrypted:
                    continue
                if n != in_pages:
                    issues.append(f"{f}: expected {in_pages} pages, found {n}")
                    continue
                for i, page in enumerate(reader.pages, start=1):
                    rot = int(page.get("/Rotate", 0)) % 360
                    if rot != deg:
                        issues.append(f"{f}: page {i} rotate={rot}, expected {deg}")
                        break

        # crop: output dimensions should be <= input dimensions
        crop_dir = dataset_dir / "crop"
        if crop_dir.exists():
            for f in crop_dir.glob("*.pdf"):
                n, reader, decrypted = pdf_pages(f, require_decrypt=False)
                if not decrypted and reader.is_encrypted:
                    continue
                if n != in_pages:
                    issues.append(f"{f}: expected {in_pages} pages, found {n}")
                    continue
                page0 = reader.pages[0]
                w = float(page0.mediabox.width)
                h = float(page0.mediabox.height)
                if w > in_w + 0.5 or h > in_h + 0.5:
                    issues.append(
                        f"{f}: crop increased page size ({w}x{h}) vs input ({in_w}x{in_h})"
                    )

        # resize: if filename includes A4, validate page size approx A4
        resize_dir = dataset_dir / "resize"
        if resize_dir.exists():
            for f in resize_dir.glob("*.pdf"):
                if "A4" not in f.stem:
                    continue
                _, reader, decrypted = pdf_pages(f, require_decrypt=False)
                if not decrypted and reader.is_encrypted:
                    continue
                page0 = reader.pages[0]
                w = float(page0.mediabox.width)
                h = float(page0.mediabox.height)
                if abs(w - A4[0]) > 1.0 or abs(h - A4[1]) > 1.0:
                    issues.append(f"{f}: expected ~A4 size ({A4[0]}x{A4[1]}), got {w}x{h}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate demo outputs against current code.")
    parser.add_argument("--demo-dir", type=Path, default=Path("demo"))
    parser.add_argument("--artifacts-dir", type=Path, default=Path("artifacts/pdfs"))
    parser.add_argument("--password", action="append", dest="passwords", default=[])
    args = parser.parse_args()

    demo_dir: Path = args.demo_dir
    artifacts_dir: Path = args.artifacts_dir
    passwords = DEFAULT_PASSWORDS + list(args.passwords)

    if not demo_dir.exists():
        print(f"demo dir not found: {demo_dir}", file=sys.stderr)
        return 2

    checked, encrypted_unknown, file_errors = _validate_demo_files(demo_dir, passwords=passwords)
    if file_errors:
        print(f"[FAIL] demo file validation: {len(file_errors)} error(s)")
        for e in file_errors[:50]:
            print(f"  - {e}")
        if len(file_errors) > 50:
            print("  ...")
        return 1

    checked_ops, op_failures = _validate_demo_outputs_match_current_ops(
        demo_dir, artifacts_dir, passwords=passwords
    )
    if op_failures:
        print(f"[FAIL] demo text outputs mismatch: {len(op_failures)} issue(s)")
        for f in op_failures[:50]:
            print(f"  - {f}")
        if len(op_failures) > 50:
            print("  ...")
        return 1

    semantic_issues = _validate_demo_semantics(demo_dir, artifacts_dir, passwords=passwords)
    if semantic_issues:
        print(f"[FAIL] demo semantics: {len(semantic_issues)} issue(s)")
        for i in semantic_issues[:50]:
            print(f"  - {i}")
        if len(semantic_issues) > 50:
            print("  ...")
        return 1

    print(
        f"[OK] demo validated (files checked: {checked}, op outputs checked: {checked_ops}, "
        f"encrypted_unknown_password: {encrypted_unknown})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
