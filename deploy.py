#!/usr/bin/env python3
from typing import Optional

import typer

import run


def main(target_host: str, token: Optional[str] = None, server: Optional[str] = None):
    print(f"Deploying Air Admin to {target_host}")
    run.sh('zip -9 -r -q air_admin.zip install.py main.py run.py requirements.txt authorized_keys air_admin.service.j2')    
    run.ssh(target_host, 'mkdir -p air_admin')
    run.sh(f'scp air_admin.zip {target_host}:air_admin')
    env = ''
    if token:
        env = f'ON_AIR_TOKEN={token}\n'
    if server:
        env += f'ON_AIR_SERVER={server}\n'
    if env:
        run.ssh(target_host, f'echo -e "{env}" > air_admin/.env')
    run.ssh(target_host,
        'cd air_admin',
        'unzip -o air_admin.zip',
        'rm air_admin.zip',
        'python3 install.py',
    )

if __name__ == "__main__":
    typer.run(main)