from nicegui import app, ui

from .authorized_keys import AuthorizedKeysDialog
from .package import add_package, get_target_folder, read_env, show_packages, write_env
from .system import docker_prune_preview, show_disk_space


def create_page() -> None:
    @ui.page('/')
    def main_page():
        with ui.header().classes('items-center'):
            ui.label('Air Link').classes('text-4xl')

            ui.space()

            authorized_keys = AuthorizedKeysDialog()
            ui.button(icon='key', on_click=authorized_keys.open) \
                .tooltip('Manage authorized keys') \
                .props('flat round color=white')

            ui.separator().props('vertical')

            ui.input('Air Link Token', password=True, password_toggle_button=True) \
                .bind_value(app.storage.general, 'air_link_token') \
                .props('dark')
            ui.button(on_click=app.shutdown, icon='power_settings_new') \
                .tooltip('Restart Air Link') \
                .props('flat round color=white')

        with ui.row():
            ui.label('Environment variables').classes('text-2xl')
            ui.button(icon='refresh', on_click=lambda: read_env(get_target_folder())) \
                .props('flat outline').tooltip('Load environment variables')
            ui.button(icon='save', on_click=lambda: write_env(get_target_folder())) \
                .props('flat outline').tooltip('Save environment variables')
        ui.codemirror().bind_value(app.storage.general, 'env').classes('h-32 border')

        ui.label('Packages').classes('text-2xl')
        ui.input('Installation directory', value='~/robot').bind_value(app.storage.general, 'target_directory')
        show_packages()
        upload = ui.upload(auto_upload=True, on_upload=add_package).props('accept=.zip').classes('hidden')
        ui.button('Upload package', icon='upload', on_click=lambda: upload.run_method('pickFiles')).props('outline')

        ui.label('System').classes('text-2xl')
        with ui.row().classes('w-full'):
            show_disk_space()
            docker_prune_preview()
