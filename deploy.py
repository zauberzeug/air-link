#!/usr/bin/env python3
import typer
from livesync import Folder, sync

from air_link.utils import run


def main(
    target_host: str = typer.Argument(..., help='hostname or IP address of the edge device (format: user@host)'),
) -> None:
    """Deploy Air Link to an edge device."""
    print(f'Deploying Air Link to {target_host}')
    sync(Folder('air_link', f'{target_host}:~/air_link'), watch=False)
    run.ssh(target_host, 'bash -i -c "cd ~/air_link; python3 --version; python3 install.py"')


if __name__ == '__main__':
    typer.run(main)
