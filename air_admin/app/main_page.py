from nicegui import app, ui

from .authorized_keys import AuthorizedKeysDialog


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
