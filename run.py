import logging
import os
import subprocess

python_cmd = 'python3'
sudo_password = ''

def sh(*cmds) -> bool:
    env = os.environ.copy()
    for cmd in cmds:
        if cmd.startswith('sudo '):
            if not sudo_password:
                logging.error('sudo password not set')
                return False
            env['SUDO_PASSWORD'] = sudo_password
            cmd = cmd.replace('sudo ', 'echo $SUDO_PASSWORD | sudo -S ', 1)
        try:
            subprocess.run(cmd, shell=True, check=True, env=env)
        except subprocess.CalledProcessError as e:
            logging.error(f'failed to run {cmd}: {e.output}')
            return False
        except Exception:
            logging.exception(f'failed to run {cmd}')
            return False   
    return True

def pip(cmd:str) -> bool:
    return sh(f'{python_cmd} -m pip {cmd}')