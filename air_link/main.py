#!/usr/bin/env python3
import logging

from app import create_main_page, setup_ssh
from nicegui import app, ui

logging.basicConfig(level=logging.INFO)
logging.getLogger('watchfiles').setLevel(logging.WARNING)

if app.storage.general.get('air_link_token'):
    app.on_startup(setup_ssh)

create_main_page()

ui.run(
    title='Air Link',
    favicon='⛑',
    reload=False,
    on_air=app.storage.general.get('air_link_token', False),
)
