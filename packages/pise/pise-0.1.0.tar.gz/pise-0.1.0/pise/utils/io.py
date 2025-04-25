from contextlib import contextmanager
from pathlib import Path
import os


@contextmanager
def cd(path: Path):
    """
    一時的にカレントディレクトリを変更するコンテキストマネージャ。
    使用例:
        with cd(work_dir):
            # ここではカレントディレクトリが work_dir になる
    """
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)
