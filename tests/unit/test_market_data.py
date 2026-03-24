from pathlib import Path


def test_market_data_api_not_generated_in_current_surface() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "generated" / "api" / "market_data_api.py").is_file()


def test_market_data_wrapper_not_generated_in_current_surface() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "generated" / "wrappers" / "market_data.py").is_file()
