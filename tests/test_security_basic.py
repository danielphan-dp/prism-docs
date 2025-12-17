from pathlib import Path

from pypdf import PdfReader

from prism_docs.core.types import OutputConfig
from prism_docs.operations.basic.decrypt import DecryptOperation
from prism_docs.operations.basic.encrypt import EncryptOperation
from tests.helpers import make_pdf


def test_encrypt_and_decrypt_roundtrip(tmp_path: Path) -> None:
    src = make_pdf(tmp_path / "secure.pdf")

    enc_result = EncryptOperation().execute(
        src, OutputConfig(), password="pw", owner_password="owner"
    )
    assert enc_result.success
    assert enc_result.output_path and enc_result.output_path.exists()

    # Encrypted file should be locked
    reader = PdfReader(enc_result.output_path)
    assert reader.is_encrypted

    dec_result = DecryptOperation().execute(enc_result.output_path, OutputConfig(), password="pw")
    assert dec_result.success
    dec_reader = PdfReader(dec_result.output_path)
    assert not dec_reader.is_encrypted
    assert len(dec_reader.pages) == 1
