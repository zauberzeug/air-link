#!/usr/bin/env python3
import logging
import os

import nicegui.air
from app import create_main_page, setup_ssh
from dotenv import load_dotenv
from nicegui import app, ui

logging.basicConfig(level=logging.INFO)
load_dotenv('.env')

if 'ON_AIR_SERVER' in os.environ:
    nicegui.air.RELAY_HOST = os.environ['ON_AIR_SERVER']
    app.on_startup(setup_ssh)

create_main_page()

ui.run(favicon='⛑')
