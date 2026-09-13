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
        assert (
            snippet not in readme
        ), f"README still documents unpublished API: {snippet}"
    assert "v1.get_token()" in readme
    assert "v1.get_portal_url" in readme
    assert "v1.list_accounts" in readme
    assert (
        "https://github.com/FinaticORG/FinaticClientSDK/blob/develop/README.md"
        in readme
    )
    assert (
        "https://github.com/FinaticORG/FinaticServerSDK-Node/blob/develop/README.md"
        in readme
    )
    assert "https://finatic.dev/docs/quick-start/account-grants" in readme
    assert (
        "https://github.com/FinaticORG/FinaticConnect/blob/develop/docs/embedding.md"
        not in readme
    )
    assert "https://finatic.dev/llms.txt" in readme
    assert "https://finatic.dev/AGENTS.md" in readme
    assert "https://finatic.dev/openapi.json" in readme


def test_readme_quick_start_is_standalone_python() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quick_start = readme.split("```python", maxsplit=1)[1].split("```", maxsplit=1)[0]
    compile(quick_start, "README.md quick start", "exec")


def test_public_init_docstring_uses_published_v1_methods() -> None:
    init_module = (ROOT / "finatic_server_python" / "__init__.py").read_text(
        encoding="utf-8"
    )
    for snippet in FORBIDDEN_SNIPPETS:
        assert (
            snippet not in init_module
        ), f"finatic_server_python.__init__ still documents unpublished API: {snippet}"
    assert "v1.get_token()" in init_module


def test_readme_guards_authenticated_session_before_account_reads() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    authenticated_session = readme.index(
        "authed = await finatic.v1.start_session(user_id=portal_user_id)"
    )
    authenticated_session_guard = readme.index('if not authed.get("session_id"):')
    account_read = readme.index(
        "accounts = await finatic.v1.list_accounts(include_sync_status=True)"
    )
    assert authenticated_session < authenticated_session_guard < account_read
    assert (
        'raise RuntimeError(authed.get("error") or "Authenticated session start failed")'
        in readme
    )
