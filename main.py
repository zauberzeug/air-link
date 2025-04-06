#!/usr/bin/env python3
import os

from air_link import main

os.environ['NICEGUI_STORAGE_PATH'] = '.air-link'

if __name__ == '__main__':
    main()
