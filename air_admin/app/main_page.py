from nicegui import app, ui

from .authorized_keys import AuthorizedKeysDialog
from .package import PACKAGES_PATH, find_packages, install_package


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
            zips = find_packages()
            if zips:
                for name in zips:
                    with ui.card().props('flat bordered'):
                        ui.label(name)
                        ui.button('Install', icon='sym_o_deployed_code_update',
                                  on_click=lambda name=name: install_package(PACKAGES_PATH / name)) \
                            .props('flat dense')
            else:
                ui.label('No packages found.')
