#!/usr/bin/env python3
import typer
from livesync import Folder, sync

from air_admin.utils import run


def main(target_host: str) -> None:
    print(f'Deploying Air Admin to {target_host}')
    sync(Folder('air_admin', f'{target_host}:~/air_admin'), watch=False)
    run.ssh(target_host, 'bash -i -c "cd ~/air_admin; python3 --version; python3 install.py"')


if __name__ == '__main__':
    typer.run(main)
