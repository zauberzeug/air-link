from __future__ import annotations

import asyncio
import logging
import os
import re
import shlex
import shutil
import zipfile
from pathlib import Path

from nicegui import app, events, ui

PACKAGES_PATH = Path('~/packages').expanduser()
PACKAGES_PATH.mkdir(exist_ok=True)
CURRENT_VERSION_PATH = Path(PACKAGES_PATH / 'current_version.txt')


def sorted_nicely(paths: list[Path]) -> list[Path]:
    # https://stackoverflow.com/a/2669120/3419103
    return sorted(paths, key=lambda path: [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', path.stem)])


def get_target_folder() -> Path | None:
    target_folder_name = app.storage.general.get('target_directory', False)
    if not target_folder_name:
        return None
    target_folder = Path(target_folder_name).expanduser()
    return target_folder


def write_env() -> None:
    target_folder = get_target_folder()
    if target_folder is None:
        ui.notify('Please set the installation directory first', type='negative')
        return
    target_folder.mkdir(exist_ok=True)
    Path(target_folder / '.env').write_text(app.storage.general.get('env', ''))


def read_env() -> None:
    target_folder = get_target_folder()
    if target_folder is None:
        ui.notify('Please set the installation directory first', type='negative')
        return
    if not target_folder.exists():
        ui.notify('Installation directory not found', type='negative')
        return
    file_path = Path(target_folder / '.env')
    if not file_path.exists():
        file_path.touch()
    app.storage.general['env'] = file_path.read_text()


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


async def add_package(event: events.UploadEventArguments) -> None:
    Path(PACKAGES_PATH / event.file.name).write_bytes(await event.file.read())
    show_packages.refresh()


def remove_package(path: Path) -> None:
    path.unlink()
    show_packages.refresh()


async def install_package(path: Path) -> None:
    target_folder = get_target_folder()
    if not target_folder:
        ui.notify('Please set the installation directory first', type='negative')
        return
    target_folder.mkdir(exist_ok=True)
    logging.info(f'Extracting {path}...')
    shutil.rmtree(target_folder)
    with zipfile.ZipFile(path, 'r') as zip_ref:
        members = zip_ref.infolist()
        for member in members:
            extracted_path = zip_ref.extract(member, target_folder)
            os.chmod(extracted_path, member.external_attr >> 16)
    logging.info('...done!')

    write_env()

    logging.info('Running install script...')
    with ui.dialog(value=True).props('maximized persistent') as dialog, ui.card():
        with ui.row().classes('w-full items-center'):
            ui.label(f'Installing {path.stem}...').classes('text-2xl')
            spinner = ui.spinner(type='gears', size='md', color='gray-500')
            ui.space()
            close_button = ui.button(icon='close', on_click=dialog.close).props('flat round color=gray-500')
            close_button.visible = False
        log = ui.log(max_lines=1000).classes('h-full')
        returncode = await run_sh(f'cd {shlex.quote(str(target_folder))} && ./install.sh', log)
        spinner.visible = False
        close_button.visible = True
        if returncode == 0:
            ui.notification('Installation complete', icon='done', type='positive')
        else:
            ui.notification(f'Installation failed with exit code {returncode}', icon='error', type='negative')
    logging.info('...done!')

    if returncode == 0:
        CURRENT_VERSION_PATH.write_text(f'./{path.name}')


async def run_sh(command: str, log: ui.log) -> int:
    process = await asyncio.create_subprocess_shell(command,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.STDOUT)
    assert process.stdout is not None

    async def read_output(stdout: asyncio.StreamReader) -> None:
        buffer = b''
        while chunk := await stdout.read(65536):  # NOTE: readline() would raise ValueError past its 64 KiB limit
            *lines, buffer = (buffer + chunk).split(b'\n')
            for line in lines:
                log.push(line.decode(errors='replace'))
        if buffer:
            log.push(buffer.decode(errors='replace'))

    reader = asyncio.create_task(read_output(process.stdout))
    while process.returncode is None:
        # process.wait() would only return once every pipe is closed, which a background child can prevent forever
        await asyncio.sleep(0.1)
    try:
        # a background child of the script may keep the pipe open forever, so only wait briefly for remaining output
        await asyncio.wait_for(reader, timeout=1.0)
    except asyncio.TimeoutError:
        pass
    return process.returncode
