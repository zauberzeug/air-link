import logging
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import List

from nicegui import app, events, run, ui

PACKAGES_PATH = Path('~/packages').expanduser()
PACKAGES_PATH.mkdir(exist_ok=True)
CURRENT_VERSION_PATH = Path(PACKAGES_PATH / 'current_version.txt')


def sorted_nicely(paths: List[Path]) -> List[Path]:
    # https://stackoverflow.com/a/2669120/3419103
    return sorted(paths, key=lambda path: [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', path.stem)])


def write_env(target_folder: Path) -> None:
    Path(target_folder / '.env').write_text(app.storage.general.get('env', ''))


def read_env(target_folder: Path) -> None:
    file_path = Path(target_folder / '.env')
    if not file_path.exists():
        file_path.touch()
    app.storage.general['env'] = file_path.read_text()


def get_target_folder() -> Path:
    target_folder = Path(app.storage.general['target_directory']).expanduser()
    target_folder.mkdir(exist_ok=True)
    return target_folder


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


async def install_package(path: Path) -> None:
    logging.info(f'Extracting {path}...')
    target = get_target_folder()
    shutil.rmtree(target)
    with zipfile.ZipFile(path, 'r') as zip_ref:
        members = zip_ref.infolist()
        for member in members:
            extracted_path = zip_ref.extract(member, target)
            os.chmod(extracted_path, member.external_attr >> 16)
    logging.info('...done!')

    write_env(target)

    logging.info('Running install script...')
    with ui.dialog(value=True).props('maximized persistent') as dialog, ui.card():
        with ui.row().classes('w-full items-center'):
            ui.label(f'Installing {path.stem}...').classes('text-2xl')
            spinner = ui.spinner(type='gears', size='md', color='gray-500')
            ui.space()
            close_button = ui.button(icon='close', on_click=dialog.close).props('flat round color=gray-500')
            close_button.visible = False
        log = ui.log().classes('h-full')
        await run_sh(f'cd {target}; ./install.sh', log)
        spinner.visible = False
        close_button.visible = True
        ui.notification('Installation complete', icon='done', type='positive')
    logging.info('...done!')

    CURRENT_VERSION_PATH.write_text(f'./{path.name}')


async def run_sh(command: str, log: ui.log) -> None:
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        assert process.stdout is not None
        assert process.stderr is not None
        while True:
            output = await run.io_bound(process.stdout.readline)
            if output == '' and process.poll() is not None:
                break
            log.push(output)
        log.push(process.stderr.read())
        ui.run_javascript(f'getElement({log.id}).scrollTop = getElement({log.id}).scrollHeight')
