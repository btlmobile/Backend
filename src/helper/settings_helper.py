import os
import yaml
from typing import Any, Dict


def load_settings(path: str = None) -> Dict[str, Any]:
    path = path or os.path.join(os.path.dirname(__file__), "..", "settings.yaml")
    path = os.path.abspath(path)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
