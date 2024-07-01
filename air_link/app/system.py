import shutil

from nicegui import ui


@ui.refreshable
def show_disk_space() -> ui.label:
    total, _, free = shutil.disk_usage('/')
    label = ui.label(f'Free disk space: {free / 2**30:.1f} GB / {total / 2**30:.1f} GB')
    if free / total < 0.1:
        return label.classes('text-negative').tooltip(f'Low disk space! {free / total:.1%} left')
    return label
