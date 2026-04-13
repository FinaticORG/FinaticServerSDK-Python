from pathlib import Path


def test_session_api_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "src" / "openapi" / "generated" / "api" / "session_api.py").is_file()


def test_session_wrapper_file_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "src" / "wrappers" / "session.py").is_file()
