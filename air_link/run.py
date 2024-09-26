import logging

from nicegui import app, ui

from .main_page import create_page
from .package import read_env
from .ssh import setup


def run() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('watchfiles').setLevel(logging.WARNING)

    on_air = app.storage.general.get('air_link_token', False)
    if on_air:
        app.on_startup(setup)

    create_page()
    app.on_startup(read_env)
    ui.run(title='Air Link', favicon='⛑', reload=False, on_air=on_air, show=False)
