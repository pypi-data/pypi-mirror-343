from pise.core.job_base import BaseJob
from pise.core.job_input import generate_vasp_input
from pise.analysis.plot_band import plot_band
from pymatgen.io.vasp import Vasprun
import json
from typing import Tuple


class BandJob(BaseJob):
    def make_vasp_input(self):
        generate_vasp_input(
            work_dir=self.work_dir,
            task="band",
            prev_dir="opt"
        )

    def analyze(self, y_range: Tuple[float, float] = (-5.0, 5.0)):
        """
        Analyze band structure:
        - plot band diagram (band.pdf/png)
        - extract bandgap, VBM, CBM
        - save all info to band_result.json

        Parameters
        ----------
        y_range : tuple of float, optional
            Energy range for band structure plot. Default is (-5, 5).
        """
        vasprun_path = self.work_dir / "vasprun.xml"
        kpoints_path = self.work_dir / "KPOINTS"
        output_base = self.work_dir / "band"

        try:
            # バンド構造プロット（PDF/PNG）
            plot_band(
                vasprun_path=vasprun_path,
                kpoints_path=kpoints_path,
                output_base=output_base,
                y_range=y_range,
                formats=["pdf", "png"]
            )
            self.logger.info(f"Band plots saved with y_range={y_range}.")

            # bandgap, vbm, cbm の抽出
            vasprun = Vasprun(str(vasprun_path))
            bs = vasprun.get_band_structure()
            bandgap_info = bs.get_band_gap()
            vbm_info = bs.get_vbm()
            cbm_info = bs.get_cbm()

            bandgap_result = {
                "bandgap": bandgap_info["energy"],
                "direct": bandgap_info["direct"],
                "vbm": vbm_info["energy"],
                "cbm": cbm_info["energy"]
            }

            with open(self.work_dir / "band_result.json", "w") as f:
                json.dump(bandgap_result, f, indent=2)

            self.logger.info("Band structure analysis complete.")

        except Exception as e:
            self.logger.error(f"BandJob analysis failed: {e}")

