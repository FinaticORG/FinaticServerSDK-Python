from pathlib import Path


def test_session_bootstrap_lives_on_v1_client() -> None:
    root = Path(__file__).resolve().parents[2]
    v1_source = (root / "src" / "v1.py").read_text(encoding="utf-8")
    assert "async def start_session" in v1_source
    assert "async def get_portal_url" in v1_source


def test_legacy_session_wrapper_removed() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "wrappers" / "session.py").is_file()
