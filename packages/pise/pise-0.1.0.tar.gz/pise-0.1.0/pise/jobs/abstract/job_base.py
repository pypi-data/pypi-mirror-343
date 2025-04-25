from abc import ABC, abstractmethod
from pathlib import Path
from pymatgen.core import Structure

from pise.core.job_status import JobStatusManager
from pise.core.job_script import JobScriptGenerator
from pise.core.job_convergence import ConvergenceChecker
from pise.core.job_submitter import JobSubmitter
from pise.utils.logger import get_logger
from pise.config.environment import Environment


class BaseJob(ABC):
    def __init__(
        self,
        work_dir: Path,
        structure: Structure,
        functional: str,
        resource: str
    ):
        """
        Abstract base class for VASP-based calculation jobs.
        Handles job state management, script generation, submission, and convergence checking.
        """
        self.work_dir = Path(work_dir)
        self.structure = structure
        self.functional = functional
        self.resource = resource
        self.job_script_name = "run_vasp.sh"
        self.logger = get_logger(self.__class__.__name__)

        # Load environment settings (submit command etc.)
        env = Environment.load()
        self.submit_command = env.submit_command

        # Initialize job components
        self.status_manager = JobStatusManager(self.work_dir / "status.json")
        self.script_generator = JobScriptGenerator(self.work_dir, self.resource, self.job_script_name)
        self.convergence_checker = ConvergenceChecker(self.work_dir)
        self.submitter = JobSubmitter(self.work_dir, self.submit_command, self.job_script_name)

        # Ensure working directory exists
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def is_converged(self) -> bool:
        """Check if job is marked as converged in status.json"""
        return self.status_manager.get("converged")

    def is_submitted(self) -> bool:
        """Check if job is marked as submitted in status.json"""
        return self.status_manager.get("submitted")

    def make_job_script(self):
        """Generate run_vasp.sh using cluster-specific template"""
        self.script_generator.generate()

    def submit(self):
        """Submit the job to the cluster, unless already submitted"""
        if self.is_submitted():
            self.logger.info("Job already submitted. Skipping.")
            return

        if self.submitter.submit():
            self.status_manager.set("submitted", True)

    def check_convergence(self):
        """Check VASP convergence and update status.json accordingly"""
        if self.is_converged():
            self.logger.info("Already marked as converged.")
            return

        if self.convergence_checker.check():
            self.status_manager.set("converged", True)

    @abstractmethod
    def make_vasp_input(self):
        """Generate VASP input files (e.g., INCAR, KPOINTS, POSCAR, POTCAR)"""
        pass

    @abstractmethod
    def analyze(self):
        """Parse calculation outputs and extract results"""
        pass

