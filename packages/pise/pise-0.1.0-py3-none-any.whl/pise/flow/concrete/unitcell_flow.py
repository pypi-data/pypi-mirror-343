from pathlib import Path
from pymatgen.core import Structure
from pise.jobs.opt import OptJob
from pise.jobs.band import BandJob

class UnitcellFlow:
    def __init__(self, base_dir: Path, structure: Structure, material_id: str, functional: str = "pbesol"):
        self.base_dir = base_dir
        self.structure = structure
        self.material_id = material_id
        self.functional = functional

        self.opt_job = OptJob(
            work_dir=base_dir / "opt",
            structure=structure,
            functional=functional,
            resource="120"
        )

        self.band_job = BandJob(
            work_dir=base_dir / "band",
            structure=None,  # structure は generate_vasp_input(prev_dir="opt") で自動取得
            functional=functional,
            resource="120"
        )

    def run(self):
        self.opt_job.load_structure_from_material_id(self.material_id)
        self.opt_job.make_vasp_input()
        self.opt_job.make_job_script()
        self.opt_job.submit()

        # convergence確認 → BandJobへ
        if self.opt_job.is_converged():
            self.band_job.make_vasp_input()
            self.band_job.make_job_script()
            self.band_job.submit()
        else:
            print("OptJob is not converged. BandJob will not be submitted.")
