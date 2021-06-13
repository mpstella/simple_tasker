## Build

Ensure you have [poetry](https://python-poetry.org/) installed on your system

```text
$> poetry shell

$> poetry install
```

## Run

To execute

```text
$> poetry run tasker -c <config_path>

$> # for example, to use the supplied configuration

$> poetry run tasker -c task.conf
```

```text
$> poetry run tasker --help
Usage: tasker [OPTIONS]

Options:
  -c, --config TEXT  Path to task configuration  [required]
  --help             Show this message and exit.
```
