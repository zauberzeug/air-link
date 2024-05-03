#!/usr/bin/env python3
import logging
import os
import sys

import icecream
import nicegui.air
from dotenv import load_dotenv
from nicegui import app, ui

from air_admin import create_main_page, setup_ssh

logging.basicConfig(level=logging.INFO)
icecream.install()
load_dotenv('.env')

if 'ON_AIR_SERVER' in os.environ:
    nicegui.air.RELAY_HOST = os.environ['ON_AIR_SERVER']

if not os.environ.get('ON_AIR_TOKEN'):
    print('Could not start: ON_AIR_TOKEN environment variable not set and not provided in .env file')
    sys.exit(1)

app.on_startup(setup_ssh)

create_main_page()

ui.run(favicon='⛑', storage_secret='secret', on_air=os.environ.get('ON_AIR_TOKEN'), reload=True)
