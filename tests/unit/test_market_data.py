from pathlib import Path


def test_market_data_api_not_generated_in_current_surface() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "generated" / "api" / "market_data_api.py").is_file()


def test_market_data_wrapper_not_generated_in_current_surface() -> None:
    root = Path(__file__).resolve().parents[2]
    assert not (root / "src" / "generated" / "wrappers" / "market_data.py").is_file()


def test_beta_generated_clients_not_shipped_in_current_surface() -> None:
    root = Path(__file__).resolve().parents[2]
    api_dir = root / "src" / "openapi" / "finatic_server" / "api"
    model_dir = root / "src" / "openapi" / "finatic_server" / "models"

    removed_api_modules = {
        "brokers_api.py",
        "company_api.py",
        "core_api.py",
        "mcp_api.py",
        "mt_connectors_api.py",
        "owner_portal_api.py",
        "portal_api.py",
        "telemetry_api.py",
    }
    for filename in removed_api_modules:
        assert not (api_dir / filename).is_file()

    forbidden_model_fragments = (
        "api_beta",
        "legacy",
        "broker_connection",
        "user_broker_connection",
        "position_lot",
    )
    remaining_models = [path.name for path in model_dir.glob("*.py")]
    assert not [
        filename
        for filename in remaining_models
        if any(fragment in filename for fragment in forbidden_model_fragments)
    ]
