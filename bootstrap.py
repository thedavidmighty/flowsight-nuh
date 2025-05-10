# bootstrap.py
"""
Create the full FlowSight NUH project skeleton in a single run.
Re-run safely: it never overwrites non-empty files.
"""

import os
from pathlib import Path

PACKAGE = "flowsight"                 # import path: src/flowsight/...

FILES = [

    # ---------- Git / CI ----------
    ".gitignore",
    ".github/workflows/ci.yml",

    # ---------- Environment ----------
    "requirements.txt",

    # ---------- Package source ----------
    f"src/{PACKAGE}/__init__.py",
    f"src/{PACKAGE}/etl/__init__.py",
    f"src/{PACKAGE}/etl/ingest.py",
    f"src/{PACKAGE}/features/__init__.py",
    f"src/{PACKAGE}/features/feature_builder.py",
    f"src/{PACKAGE}/models/__init__.py",
    f"src/{PACKAGE}/models/train.py",
    f"src/{PACKAGE}/models/forecast.py",
    f"src/{PACKAGE}/viz/__init__.py",
    f"src/{PACKAGE}/viz/spc_chart.py",
    f"src/{PACKAGE}/config/__init__.py",
    f"src/{PACKAGE}/config/logging.yaml",

    # ---------- Notebooks ----------
    "notebooks/eda.ipynb",
    "notebooks/model_dev.ipynb",

    # ---------- Data & artefacts (git-kept placeholders) ----------
    "data/.gitkeep",
    "data/raw/.gitkeep",
    "data/curated/.gitkeep",
    "outputs/.gitkeep",
    "mlruns/.gitkeep",

    # ---------- Tests ----------
    "tests/unit/__init__.py",
    "tests/unit/test_smoke.py",
    "tests/integration/__init__.py",

    # ---------- Docs ----------
    "docs/README_project.md",

    # ---------- Project meta ----------
    "README.md",
    "LICENSE",
    "pyproject.toml",
]

def touch(filepath: Path) -> None:
    """Create an empty file unless it already exists and is non-zero."""
    if filepath.exists() and filepath.stat().st_size > 0:
        return
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.touch()

def main() -> None:
    for fp in FILES:
        touch(Path(fp))
    print("✅  FlowSight NUH skeleton created.")

if __name__ == "__main__":
    main()
