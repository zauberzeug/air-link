#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

from air_link import main

os.environ['NICEGUI_STORAGE_PATH'] = '.air-link'

old_storage_path = Path('.nicegui/general-storage.json')
new_storage_path = Path('.air-link/general-storage.json')

if old_storage_path.exists() and not new_storage_path.exists():
    try:
        new_storage_path.parent.mkdir(exist_ok=True)
        shutil.copy(old_storage_path, new_storage_path)
        print('Migrated storage from .nicegui to .air-link')
    except Exception as e:
        print(f'Error migrating storage: {e}')


if __name__ == '__main__':
    main()
