from pathlib import Path
import subprocess
from pise.utils.logger import get_logger
from pise.utils.io import cd


class JobSubmitter:
    def __init__(self, work_dir: Path, submit_command: str, job_script_name: str = "run_vasp.sh"):
        self.work_dir = work_dir
        self.submit_command = submit_command
        self.job_script_name = job_script_name
        self.logger = get_logger(self.__class__.__name__)

    def submit(self) -> bool:
        with cd(self.work_dir):
            try:
                subprocess.run(
                    f"{self.submit_command} {self.job_script_name}",
                    shell=True,
                    check=True
                )
                self.logger.info(f"Job submitted: {self.submit_command} {self.job_script_name}")
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Submission failed: exit code {e.returncode}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
            return False

