from pathlib import Path
from typing import Optional, Dict
from pymatgen.io.vasp.inputs import Poscar

def get_composition_info(work_dir: Path) -> Dict[str, Optional[object]]:
    path = work_dir / "POSCAR-finish"
    if path.exists():
        structure = Poscar.from_file(str(path)).structure
        comp = structure.composition
        return {
            "composition": comp.as_dict(),
            "formula": comp.reduced_formula
        }
    return {"composition": None, "formula": None}
