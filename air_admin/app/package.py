import logging
import re
import shutil
import zipfile
from pathlib import Path
from typing import List

from nicegui import app
from utils import run

PACKAGES_PATH = Path('~/packages').expanduser()
PACKAGES_PATH.mkdir(exist_ok=True)

TARGET = Path('~/robot').expanduser()


def sorted_nicely(list_: List[str]) -> List[str]:
    # https://stackoverflow.com/a/2669120/3419103
    return sorted(list_, key=lambda key: [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', key)])


def find_packages() -> List[str]:
    return sorted_nicely([path.name for path in PACKAGES_PATH.glob('*.zip')])


def install_package(path: Path) -> None:
    logging.info(f'Extracting {path}...')
    shutil.rmtree(TARGET)
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(TARGET)
    logging.info('...done!')

    Path(TARGET / '.env').write_text(app.storage.general.get('env', ''))

    logging.info('Running install script...')
    run.sh(f'cd {TARGET}', './install.sh')
    logging.info('...done!')

    Path(PACKAGES_PATH / 'current_version.txt').write_text(f'./{path.name}')
