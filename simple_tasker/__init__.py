__version__ = '0.1.0'

from contextlib import contextmanager
import inspect
import logging
import os
from pathlib import Path
from typing import Dict, Generator, List
from pyhocon import ConfigFactory

from simple_tasker.tasks import registry

def get_mandatory_args(func) -> List[str]:

    mandatory_args = []
    for k, v in inspect.signature(func).parameters.items():
        if (
            k != "self"
            and v.default is inspect.Parameter.empty
            and not str(v).startswith("*")
        ):
            mandatory_args.append(k)

    return mandatory_args

@contextmanager
def wrap_environment(env: Dict[str, str] = None) -> Generator[None, None, None]:

    _env = os.environ.copy()
    os.environ.update(env or {})
    yield
    os.environ.clear()
    os.environ.update(_env)


class Tasker:

    def __init__(self, path: Path, env: Dict[str, str] = None) -> None:
    
        self.logger = logging.getLogger(self.__class__.__name__)
        self._tasks = []

        with wrap_environment(env):
            self._config = ConfigFactory.parse_file(path)
    
    
    def __validate_config(self) -> bool:
        
        error_count = 0

        for task in self._config.get("tasks", []):
            name, args = task["name"].lower(), task.get("args", {})

            if registry.has(name):
                for arg in get_mandatory_args(registry.get(name).run):
                    if arg not in args:
                        print(f"Missing arg '{arg}' for task '{name}'")
                        error_count += 1
            else:
                print(f"Unknown tasks '{name}'")
                error_count += 1

            self._tasks.append((name, args))

        return error_count == 0

    def run(self) -> bool:

        if self.__validate_config():

            for name, args in self._tasks:
                exe = registry.create(name)
                self.logger.info(f"About to execute: '{name}'")
                if not exe.run(**args):
                    self.logger.error(f"Failed tasks '{name}'")
                    return False

            return True
        return False