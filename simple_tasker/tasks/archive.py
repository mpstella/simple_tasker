import tarfile
import os
from simple_tasker.tasks import Task


class Archive(Task):

    def __init__(self) -> None:
        super().__init__()

    def run(self, input_directory_path: str, target_file_path: str) -> bool:

        self.logger.info(f"Archiving '{input_directory_path}' to '{target_file_path}'")

        with tarfile.open(target_file_path, "w:gz") as tar:
            tar.add(
                input_directory_path, arcname=os.path.basename(input_directory_path)
            )
        return True
