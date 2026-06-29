from pathlib import Path


def test_legacy_brokers_wrapper_removed() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "wrappers" / "brokers.py").is_file()
