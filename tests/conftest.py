# tests/conftest.py
"""`src/` on the path, so the tests import what the package ships.

`pyproject.toml` declares the wheel's packages as `src/scripts`, and this
record is not installed into the environment that runs its own tests.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
