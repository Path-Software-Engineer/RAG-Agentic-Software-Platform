from __future__ import annotations

import json
import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SERVICE_ROOT.parents[1]
sys.path.insert(0, str(SERVICE_ROOT))

from app.main import app  # noqa: E402


def main() -> None:
    output_directory = PROJECT_ROOT / "packages" / "contracts" / "openapi"
    output_directory.mkdir(parents=True, exist_ok=True)
    (output_directory / "internal-v1.json").write_text(
        json.dumps(app.openapi(), indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
