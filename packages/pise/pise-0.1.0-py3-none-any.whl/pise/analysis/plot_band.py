from pathlib import Path
from typing import Tuple
from pymatgen.io.vasp import Vasprun
from vise.analyzer.bands import BandPlotInfoFromVasp
from vise.plot.band_plotter import BandMplPlotter


def plot_band(
    vasprun_path: Path,
    kpoints_path: Path,
    output_path: Path,
    y_range: Tuple[float, float] = (-5.0, 5.0)
):
    """
    Plot band structure using VASP output and save as PDF.

    Parameters
    ----------
    vasprun_path : Path
        Path to vasprun.xml
    kpoints_path : Path
        Path to KPOINTS file
    output_path : Path
        Where to save the PDF plot (e.g., band.pdf)
    y_range : Tuple[float, float]
        Energy window to display in the plot (e.g., (-5, 5))
    """
    vasprun = Vasprun(str(vasprun_path))
    band_info = BandPlotInfoFromVasp(
        vasprun=vasprun,
        kpoints_filename=str(kpoints_path)
    ).make_band_plot_info()

    band_info.to_json_file()
    plotter = BandMplPlotter(band_info, energy_range=y_range)
    plotter.construct_plot()
    plotter.plt.savefig(output_path, format="pdf")

