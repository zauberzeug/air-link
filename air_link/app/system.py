import shutil

from nicegui import ui


def get_disk_space() -> tuple[float, float]:
    total, _, free = shutil.disk_usage('/')
    return total / 2**30, free / 2**30


@ui.refreshable
def show_disk_space() -> ui.label:
    total, free = get_disk_space()
    label = ui.label(f'Free disk space: {free:.1f} GB / {total:.1f} GB')
    if free / total < 0.1:
        return label.classes('text-negative').tooltip(f'Low disk space! {free / total * 100:.1f}% left')
    return label
