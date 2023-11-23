import logging
import os
import subprocess

python_cmd = 'python3'
sudo_password = ''

def sh(*cmds:str) -> bool:
    for cmd in cmds:
        if cmd.startswith('sudo '):
            logging.error('sudo not allowed in sh(), use run.sudo() instead')
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f'failed to run {cmd}: {e.output}')
            return False
        except Exception:
            logging.exception(f'failed to run {cmd}')
            return False   
    return True

def pip(cmd:str) -> bool:
    return sh(f'{python_cmd} -m pip {cmd}')

def sudo(*cmds:str) -> bool:
    if not sudo_password:
        logging.error('sudo password not set; we suggest: sudo_password = getpass.getpass(prompt="Enter sudo password: ")')
        return False
    for cmd in cmds:
        try:
            cmd = f'sudo -S {cmd}'
            print(f'running {cmd}', flush=True)
            process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
            stdout, stderr = process.communicate(input=sudo_password + '\n')
            if process.wait() != 0:
                logging.error(f'failed to run {cmd}: {stdout}\n{stderr}')
                return False
        except subprocess.CalledProcessError as e:
            logging.error(f'failed to run {cmd}: {e.output}')
            return False
        except Exception as e:
            logging.exception(f'failed to run {cmd}: {str(e)}')
            return False
    return True

def ssh(target_host:str, *cmds:str) -> bool:
    cmd_chain = ' && '.join(cmds)
    return sh(f'ssh -t {target_host} \'{cmd_chain}\'')