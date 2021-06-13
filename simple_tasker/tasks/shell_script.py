from simple_tasker.tasks import Task
from typing import List, Union

import subprocess

class ShellScript(Task):

    task_name = "shell_script"

    def __init__(self) -> None:
        super().__init__()
    
    def run(
        self,
        script_path: str,
        script_args: Union[str, List[str]] = None,
        working_directory_path: str = None
    ) -> bool:    

        cmd = [script_path]

        if isinstance(script_args, str):
            cmd.append(script_args)
        else:
            cmd += script_args

        try:
        
            result = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                cwd=working_directory_path
            ).decode("utf-8").splitlines()
        
            for o in result:               
                self.logger.info(o)

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.logger.error(e)
            return False

        return True
