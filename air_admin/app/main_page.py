import re
from pathlib import Path
from typing import List

from nicegui import app, ui

from .authorized_keys import AuthorizedKeysDialog
from .package import install

PACKAGES_PATH = Path('~/packages').expanduser()
PACKAGES_PATH.mkdir(exist_ok=True)


def sorted_nicely(list_: List[str]) -> List[str]:
    # https://stackoverflow.com/a/2669120/3419103
    return sorted(list_, key=lambda key: [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', key)])


def create_page() -> None:
    @ui.page('/')
    def main_page():
        with ui.header().classes('items-center'):
            ui.label('Air Admin').classes('text-4xl')

            ui.space()

            authorized_keys = AuthorizedKeysDialog()
            ui.button(icon='key', on_click=authorized_keys.open) \
                .tooltip('Manage authorized keys') \
                .props('flat round color=white')

            ui.separator().props('vertical')

            ui.input('Air Admin Token', password=True, password_toggle_button=True) \
                .bind_value(app.storage.general, 'air_admin_token') \
                .props('dark')
            ui.button(on_click=app.shutdown, icon='power_settings_new') \
                .tooltip('Restart Air Admin') \
                .props('flat round color=white')

        ui.label('Environment variables').classes('text-2xl')
        ui.codemirror().bind_value(app.storage.general, 'env').classes('h-32 border')

        ui.label('Packages').classes('text-2xl')
        with ui.row():
            zips = sorted_nicely([path.name for path in PACKAGES_PATH.glob('*.zip')])
            if zips:
                for name in zips:
                    with ui.card().props('flat bordered'):
                        ui.label(name)
                        ui.button('Install', icon='sym_o_deployed_code_update',
                                  on_click=lambda name=name: install(name)) \
                            .props('flat dense')
            else:
                ui.label('No packages found.')
