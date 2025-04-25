from pathlib import Path
from typing import Optional
from pymatgen.io.vasp.outputs import Outcar

def get_final_energy(work_dir: Path) -> Optional[float]:
    path = work_dir / "OUTCAR-finish"
    if path.exists():
        return Outcar(str(path)).final_energy
    return None
