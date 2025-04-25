from pathlib import Path
import json
from typing import Any

DEFAULT_STATUS = {
    "prepare": False,
    "converged": False,
    "analyze": False,
    "submitted": False
}


class JobStatusManager:
    def __init__(self, path: Path):
        self.path = path
        self.status = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return DEFAULT_STATUS.copy()
        with open(self.path) as f:
            loaded = json.load(f)
        return {**DEFAULT_STATUS, **loaded} 

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self.status, f, indent=2)

    def get(self, key: str, default: Any = False) -> Any:
        return self.status.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.status[key] = value
        self.save()
