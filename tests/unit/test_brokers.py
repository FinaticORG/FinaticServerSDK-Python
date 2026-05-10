from pathlib import Path


def test_brokers_api_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (
        root / "src" / "openapi" / "finatic_server" / "api" / "brokers_api.py"
    ).is_file()


def test_brokers_wrapper_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "src" / "wrappers" / "brokers.py").is_file()
