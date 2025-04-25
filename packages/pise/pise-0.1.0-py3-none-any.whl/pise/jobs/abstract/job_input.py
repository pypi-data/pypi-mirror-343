# core/job_input.py

from types import SimpleNamespace
from pathlib import Path
from typing import Optional, Union, List
from vise.cli.main_functions import VaspSet
from vise.input_set.task import Task
from vise.input_set.xc import Xc
from vise.defaults import defaults


def generate_vasp_input(
    work_dir: Path,
    xc: Optional[Union[Xc, str]] = None,
    task: Optional[Union[Task, str]] = None,
    poscar: Optional[Path] = None,
    kpt_density: Optional[float] = None,
    prev_dir: Optional[Path] = None,
    user_incar_settings: Optional[List[str]] = None,
    options: Optional[List[str]] = None,
    overridden_potcar: Optional[List[str]] = None,
    uniform_kpt_mode: bool = False,
    file_transfer_type: Optional[List[str]] = None,
    vasprun: Optional[str] = None,
    outcar: Optional[str] = None
) -> VaspSet:
    """
    Generate a VASP input set using vise.VaspSet with CLI-equivalent behavior.

    Parameters
    ----------
    work_dir : Path
        Directory to generate input files in.
    xc : str or Xc, optional
        Exchange-correlation functional.
    task : str or Task, optional
        Calculation task type.
    poscar : Path, optional
        Path to the POSCAR file. Defaults to work_dir / "POSCAR".
    kpt_density : float, optional
        K-point density. If None, it is auto-determined by VaspSet.
    prev_dir : Path, optional
        Previous calculation directory.
    user_incar_settings : list of str, optional
        INCAR settings in CLI-style pairs.
    options : list of str, optional
        Additional input options.
    overridden_potcar : list of str, optional
        Manually specified POTCAR types.
    uniform_kpt_mode : bool
        Whether to use uniform k-point sampling.
    file_transfer_type : list of str, optional
        File transfer instructions for reuse.
    vasprun : str, optional
        Filename for vasprun.xml.
    outcar : str, optional
        Filename for OUTCAR.

    Returns
    -------
    VaspSet
        Configured VaspSet instance.
    """

    poscar = poscar or work_dir / "POSCAR"
    if not poscar.exists():
        raise FileNotFoundError(f"{poscar} not found. Please create POSCAR first.")

    task = Task(task) if task is not None and not isinstance(task, Task) else task or defaults.task
    xc = Xc(xc) if xc is not None and not isinstance(xc, Xc) else xc or defaults.xc
    vasprun = vasprun or str(defaults.vasprun)
    outcar = outcar or str(defaults.outcar)
    overridden_potcar = overridden_potcar or defaults.overridden_potcar

    if user_incar_settings is None:
        user_incar_settings = [
            str(i) for pair in defaults.user_incar_settings.items() for i in pair
        ]

    args = SimpleNamespace(
        dirs=[work_dir],
        poscar=poscar,
        xc=xc,
        kpt_density=kpt_density,
        overridden_potcar=overridden_potcar,
        user_incar_settings=user_incar_settings,
        prev_dir=prev_dir,
        options=options,
        uniform_kpt_mode=uniform_kpt_mode,
        file_transfer_type=file_transfer_type,
        vasprun=vasprun,
        outcar=outcar,
        task=task
    )

    return VaspSet(args)




