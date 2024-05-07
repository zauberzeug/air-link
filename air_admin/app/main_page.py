from nicegui import app, ui


def create_page() -> None:
    @ui.page('/')
    def main_page():
        ui.label('Air Admin').classes('text-4xl')
        ui.button(on_click=app.shutdown, icon='power_settings_new')

        ui.input('Air Admin Token').bind_value(app.storage.general, 'air_admin_token')
