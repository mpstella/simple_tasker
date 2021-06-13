import glob
import logging
from abc import ABC, abstractmethod
from os.path import dirname, basename, isfile, join
from typing import List

class ClassNotRegisteredException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"missing or un registered class '{name}'")


class TaskRegistry:

    def __init__(self) -> None:
        self._registry = {}

    def register(self, cls: type) -> None:
        n = getattr(cls, 'task_name', cls.__name__).lower()
        self._registry[n] = cls

    def registered(self) -> List[str]:
        return list(self._registry.keys())

    def has(self, name: str) -> bool:
        return name in self._registry

    def get(self, name: str) -> type:
        return self._registry[name]
    
    def create(self, name: str, *args, **kwargs) -> object:
        try:
            return self._registry[name](*args, **kwargs)
        except KeyError:
            raise ClassNotRegisteredException(name)


registry = TaskRegistry()

class Task(ABC):

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def __init_subclass__(cls) -> None:
        registry.register(cls)

    @abstractmethod
    def run(self, **kwargs) -> bool:
        raise NotImplementedError

modules = glob.glob(join(dirname(__file__), "*.py"))

for f in modules:
    if isfile(f) and not f.endswith("__init__.py"):
        __import__(f"{Task.__module__}.{basename(f)[:-3]}")