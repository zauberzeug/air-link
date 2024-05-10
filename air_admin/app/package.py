import logging
import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import List

from nicegui import app, events, ui
from utils import run

PACKAGES_PATH = Path('~/packages').expanduser()
PACKAGES_PATH.mkdir(exist_ok=True)
CURRENT_VERSION_PATH = Path(PACKAGES_PATH / 'current_version.txt')

TARGET = Path('~/robot').expanduser()


def sorted_nicely(paths: List[Path]) -> List[Path]:
    # https://stackoverflow.com/a/2669120/3419103
    return sorted(paths, key=lambda path: [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', path.stem)])


@ui.refreshable
def show_packages() -> ui.row:
    paths = sorted_nicely(list(PACKAGES_PATH.glob('*.zip')))
    current_version = Path(CURRENT_VERSION_PATH.read_text()).stem if CURRENT_VERSION_PATH.exists() else None
    with ui.row(wrap=False).classes('w-full overflow-scroll') as row:
        for path in reversed(paths):
            with ui.card().tight().props('flat bordered'):
                with ui.card_section().classes('bg-blue-100' if path.stem == current_version else 'bg-gray-100'):
                    ui.label(path.stem)
                    ui.label(f'{path.stat().st_size / 1024 / 1024:.2f} MB') \
                        .classes('text-xs text-gray-500')
                with ui.card_actions():
                    with ui.dropdown_button('Install', icon='sym_o_deployed_code_update', split=True,
                                            on_click=lambda path=path: install_package(path)).props('flat'):
                        ui.menu_item('Remove', on_click=lambda path=path: remove_package(path))
    return row


def add_package(event: events.UploadEventArguments) -> None:
    Path(PACKAGES_PATH / event.name).write_bytes(event.content.read())
    show_packages.refresh()


def remove_package(path: Path) -> None:
    path.unlink()
    show_packages.refresh()


def install_package(path: Path) -> None:
    logging.info(f'Extracting {path}...')
    shutil.rmtree(TARGET)
    with zipfile.ZipFile(path, 'r') as zip_ref:
        members = zip_ref.infolist()
        for member in members:
            extracted_path = zip_ref.extract(member, TARGET)
            os.chmod(extracted_path, member.external_attr >> 16)
    logging.info('...done!')

    Path(TARGET / '.env').write_text(app.storage.general.get('env', ''))

    logging.info('Running install script...')
    run.sh(f'cd {TARGET}; ./install.sh')
    logging.info('...done!')

    CURRENT_VERSION_PATH.write_text(f'./{path.name}')
