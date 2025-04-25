import json
from pymatgen.ext.matproj import MPRester
from pise.core.job_base import BaseJob
from pise.core.job_input import generate_vasp_input
from pise.analysis.opt_job_analysis import analyze_opt_result


class OptJob(BaseJob):
    def load_structure_from_material_id(self, material_id: str):
        """
        Retrieve structure from Materials Project using the given material_id,
        and record it to opt_result.json for later tracking.
        """
        with MPRester() as mpr:
            structure = mpr.get_structure_by_material_id(material_id)
        self.structure = structure

        # Save material_id to opt_result.json
        result_path = self.work_dir / "opt_result.json"
        result = {"material_id": material_id}
        with open(result_path, "w") as f:
            json.dump(result, f, indent=2)

        self.logger.info(f"Structure loaded and material_id saved to {result_path}.")

    def make_vasp_input(self):
        """
        Generate VASP input files for structure optimization.
        Writes POSCAR if it does not already exist.
        """
        poscar_path = self.work_dir / "POSCAR"
        if not poscar_path.exists():
            self.structure.to(filename=str(poscar_path))

        generate_vasp_input(
            work_dir=self.work_dir,
            task="structure_opt",
            user_incar_settings=["ENCUT", "520"]
        )

    def analyze(self):
        """
        Analyze VASP outputs (OUTCAR-finish, POSCAR-finish) and update opt_result.json
        with final energy, composition, and reduced formula. Retains material_id.
        """
        result = analyze_opt_result(self.work_dir)

        # Restore material_id from previous result (if exists)
        result_path = self.work_dir / "opt_result.json"
        if result_path.exists():
            with open(result_path) as f:
                existing = json.load(f)
            result["material_id"] = existing.get("material_id")

        # Save updated result
        with open(result_path, "w") as f:
            json.dump(result, f, indent=2)

        self.logger.info(f"Analysis complete. Result saved to {result_path}.")



