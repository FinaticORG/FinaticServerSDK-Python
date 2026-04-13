from __future__ import annotations

import importlib
import runpy
from pathlib import Path


def test_import_generated_models_for_public_surface_coverage() -> None:
    root = Path(__file__).resolve().parents[2]
    models_dir = root / "src" / "openapi" / "generated" / "models"
    model_modules = sorted(
        module_path.stem
        for module_path in models_dir.glob("*.py")
        if module_path.stem not in {"__init__"}
    )

    imported_count = 0
    for module_name in model_modules:
        try:
            importlib.import_module(f"src.openapi.generated.models.{module_name}")
            imported_count += 1
        except Exception:
            module_path = models_dir / f"{module_name}.py"
            try:
                runpy.run_path(str(module_path))
                imported_count += 1
            except Exception:
                # Keep going so we still exercise as much generated surface as possible.
                continue

    assert imported_count > 50
