"""Partner-facing docs must match the published v1 façade."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_SNIPPETS = (
    "finatic.get_token()",
    "get_all_positions()",
    "v1.create_session()",
    "v1.create_portal_link()",
    "list_account_orders",
    "get_accounts()",
)


def test_readme_uses_published_v1_methods() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for snippet in FORBIDDEN_SNIPPETS:
        assert snippet not in readme, f"README still documents unpublished API: {snippet}"
    assert "v1.get_token()" in readme
    assert "v1.get_portal_url" in readme
    assert "v1.list_accounts" in readme
    assert "https://github.com/FinaticORG/FinaticClientSDK/blob/develop/README.md" in readme
    assert "https://finatic.dev/AGENTS.md" in readme
    assert "https://finatic.dev/openapi.json" in readme


def test_public_init_docstring_uses_published_v1_methods() -> None:
    init_module = (ROOT / "finatic_server_python" / "__init__.py").read_text(
        encoding="utf-8"
    )
    for snippet in FORBIDDEN_SNIPPETS:
        assert snippet not in init_module, (
            f"finatic_server_python.__init__ still documents unpublished API: {snippet}"
        )
    assert "v1.get_token()" in init_module
