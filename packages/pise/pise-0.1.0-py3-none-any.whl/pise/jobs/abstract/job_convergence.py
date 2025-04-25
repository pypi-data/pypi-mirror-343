from pathlib import Path
from pymatgen.io.vasp.outputs import Vasprun
from pise.utils.logger import get_logger


class ConvergenceChecker:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.logger = get_logger(self.__class__.__name__)

    def check(self) -> bool:
        vasprun_path = self.work_dir / "vasprun.xml"
        if not vasprun_path.exists():
            self.logger.warning("vasprun.xml not found.")
            return False

        try:
            vasprun = Vasprun(str(vasprun_path))
            if vasprun.converged:
                self.logger.info("Converged ✅")
                return True
            else:
                self.logger.warning("Not converged ❌")
                return False
        except Exception as e:
            self.logger.error(f"Failed to parse vasprun.xml: {e}")
            return False
