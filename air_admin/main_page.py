from nicegui import ui


def create_page() -> None:
    @ui.page('/')
    def main_page():
        ui.label('Air Admin').classes('text-4xl')
