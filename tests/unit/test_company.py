from pathlib import Path


def test_legacy_company_wrapper_removed() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "wrappers" / "company.py").is_file()
