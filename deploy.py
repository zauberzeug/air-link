#!/usr/bin/env python3
import json
import shlex
from pathlib import Path
from typing import Optional

import typer

import run


def main(target_host: str, token: Optional[str] = None, server: Optional[str] = None):
    print(f"Deploying Air Admin to {target_host}")
    python_files = ' '.join(shlex.quote(str(path)) for path in Path('.').glob('*.py'))
    run.sh(f'zip -9 -r -q air_admin.zip requirements.txt authorized_keys air_admin.service.j2 {python_files}')    
    run.ssh(target_host, 'mkdir -p air_admin')
    run.sh(f'scp air_admin.zip {target_host}:air_admin')
    env = {'AUTO_RELOAD': 'AUTO_RELOAD=false'}
    if token:
        env['ON_AIR_TOKEN'] = f'ON_AIR_TOKEN={token}'
    if server:
        env['ON_AIR_SERVER'] = f'ON_AIR_SERVER={server}'
    run.ssh(target_host,
        'cd air_admin',
        'unzip -o air_admin.zip',
        f'echo \'{json.dumps(env)}\' > env_update.json',
        'rm air_admin.zip',
        'python3 install.py',
    )

if __name__ == "__main__":
    typer.run(main)