import subprocess

python_cmd = 'python3'

def sh(cmd:str) -> bool:
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        return False
    return True

def pip(cmd:str) -> bool:
    return sh(f'{python_cmd} -m pip {cmd}')