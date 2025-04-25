import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".pise_env.json"

class Environment:
    def __init__(self, cluster, submit_command, vasp_path):
        self.cluster = cluster
        self.submit_command = submit_command
        self.vasp_path = vasp_path

    def to_dict(self):
        return {
            "cluster": self.cluster,
            "submit_command": self.submit_command,
            "vasp_path": self.vasp_path
        }

    def save(self, path: Path = CONFIG_PATH):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path = CONFIG_PATH):
        if not path.exists():
            raise FileNotFoundError(
                f"設定ファイル {path} が見つかりません。`pise init` を実行して環境設定を行ってください。"
            )
        with open(path) as f:
            config = json.load(f)
        return cls(**config)

