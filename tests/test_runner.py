from pathlib import Path

from prism_docs.core import Config
from prism_docs.core.runner import PDFRunner
from .helpers import make_pdf


def test_runner_parallel_executes_all(tmp_path: Path) -> None:
    pdf1 = make_pdf(tmp_path / "a.pdf")
    pdf2 = make_pdf(tmp_path / "b.pdf")

    config = Config()
    config.global_settings.parallel = True
    config.default_output.output_dir = tmp_path

    runner = PDFRunner(config)
    results = runner.run("compress", [pdf1, pdf2])

    assert len(results) == 2
    for res in results:
        assert res.success
        assert res.output_path and res.output_path.exists()


def test_runner_dry_run_returns_messages(tmp_path: Path) -> None:
    pdf = make_pdf(tmp_path / "c.pdf")

    config = Config()
    config.global_settings.dry_run = True

    runner = PDFRunner(config)
    results = runner.run("compress", pdf)

    assert len(results) == 1
    res = results[0]
    assert res.success
    assert res.output_path is None
    assert "[DRY RUN]" in res.message
