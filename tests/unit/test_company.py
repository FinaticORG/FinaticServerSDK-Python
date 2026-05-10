from pathlib import Path


def test_company_api_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (
        root / "src" / "openapi" / "finatic_server" / "api" / "company_api.py"
    ).is_file()


def test_company_wrapper_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "src" / "wrappers" / "company.py").is_file()
