#!/usr/bin/env python3
from typing import Optional

import typer

import run


def main(target_host: str, on_air_token: str, on_air_server: Optional[str] = None):
    print(f"Priming {target_host}")
    run.sh('zip -9 -r -q air_admin.zip install.py main.py run.py requirements.txt authorized_keys air_admin.service.j2')
    
    run.sh(f'ssh {target_host} mkdir -p air_admin')
    run.sh(f'scp air_admin.zip {target_host}:air_admin')
    env = f'ON_AIR_TOKEN={on_air_token}\n'
    if on_air_server:
        env += f'ON_AIR_SERVER={on_air_server}\n'
    remote_cmds= [
        f'echo "{env}" > air_admin/.env',
        'cd air_admin',
        'unzip -o air_admin.zip',
        'rm air_admin.zip',
        'python3 install.py',
    ]
    run.sh(f'ssh {target_host} \'{" && ".join(remote_cmds)}\'')

if __name__ == "__main__":
    typer.run(main)