import os
import click
import logging
import platform
from simple_tasker import Tasker
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-16s | %(levelname)-7s | %(message)s",
    datefmt="%d-%m-%Y %H:%M",
    filename=None,
)

env = {
    "TODAY": datetime.today().strftime("%Y-%m-%d"),
    "PLATFORM": platform.system(),
    "CWD": os.getcwd()
}

@click.command(name="SimpleFlow")
@click.option("-c", "--config", required=True, help="Path to task configuration")
def cli(config: str) -> None:

    tasker = Tasker(config, env)
    tasker.run()

if __name__ == "__main__":
    cli()