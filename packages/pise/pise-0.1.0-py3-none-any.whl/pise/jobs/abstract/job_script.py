from pathlib import Path
from pise.config.environment import Environment
from pise.utils.logger import get_logger


class JobScriptGenerator:
    def __init__(self, work_dir: Path, resource: str, job_script_name: str = "run_vasp.sh"):
        self.work_dir = work_dir
        self.resource = resource
        self.job_script_name = job_script_name
        self.logger = get_logger(self.__class__.__name__)

        env = Environment.load()
        self.cluster = env.cluster
        self.vasp_path = env.vasp_path

    def generate(self) -> Path:
        script_text = self._generate_script_text(
            cluster=self.cluster,
            resource=self.resource,
            vasp_path=self.vasp_path
        )
        script_path = self.work_dir / self.job_script_name
        script_path.write_text(script_text)
        self.logger.info(f"Job script created at {script_path.resolve()}")
        return script_path

    def _generate_script_text(self, cluster: str, resource: str, vasp_path: str) -> str:
        cluster = cluster.lower()
        if cluster == "genkai":
            return f"""#!/bin/sh
#------ pjsub option --------#
#PJM -L rscgrp=a-pj25000005
#PJM -L vnode-core={resource}
#PJM -L elapse=168:00:00
#PJM -j

if [ -f /etc/profile.d/modules.sh ]; then
  . /etc/profile.d/modules.sh
fi

module load intel/2024.1
module load impi

mpi=/home/app/inteloneapi/2024.1/mpi/2021.12/bin/mpiexec.hydra
vasp={vasp_path}

$mpi -n {resource} $vasp
"""

        elif cluster == "laurel":
            return f"""#!/bin/bash
#SBATCH -p gr10261b
#SBATCH -t 168:00:00
#SBATCH --rsc p={resource}:t=1:c=1
#SBATCH -o %x.%j.out

export MKLROOT=/opt/system/app/intel/2022.3/mkl/2022.2.0/
vasp={vasp_path}

srun $vasp
"""

        else:
            raise ValueError(f"未対応のクラスタ名です: {cluster}（genkai または laurel のみ対応）")
