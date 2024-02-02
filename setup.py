#!/usr/bin/env python
from yaml import safe_load as yaml_loads

from app_cli import Cli, Command, echo


def create_cli() -> Cli:

    cli = Cli(__file__)
    cli.add_command('get-version', get_version())

    return cli


def get_version() -> Command:

    def _version():
        with open(".config/meta.yml", encoding="utf-8") as meta:
            project = yaml_loads(meta)
            echo(project['version'])

    return Command(
        name='get-version',
        callback=_version,
        help="Print current version of application"
    )


if __name__ == '__main__':
    create_cli().start()
