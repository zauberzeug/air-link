import shutil

import docker
from nicegui import ui


@ui.refreshable
def show_disk_space() -> None:
    total, _, free = shutil.disk_usage('/')
    label = ui.label(f'Free disk space: {free / 2**30:.1f} GB / {total / 2**30:.1f} GB')
    if free / total < 0.1:
        label.classes('text-negative').tooltip(f'Low disk space! {free / total:.1%} left')


def _get_docker_client() -> docker.DockerClient | None:
    try:
        return docker.DockerClient(base_url='unix://var/run/docker.sock')
    except Exception:
        ui.notify('Could not connect to Docker API', type='negative')
        return None


def docker_prune_dry_run() -> tuple[int, int, int, int]:
    client = _get_docker_client()
    if not client:
        return 0, 0, 0, 0
    dangling_images = len(client.images.list(filters={'dangling': True}))
    stopped_containers = (len(client.containers.list(filters={'status': 'exited'})) +
                          len(client.containers.list(filters={'status': 'created'})))
    unused_volumes = len(client.volumes.list(filters={'dangling': True}))
    unused_networks = len(client.networks.list(filters={'dangling': True}))
    return dangling_images, stopped_containers, unused_volumes, unused_networks


def docker_prune(what: str) -> None:
    client = _get_docker_client()
    if not client:
        return
    match what:
        case 'images':
            result = client.images.prune()
            num_deleted = len(result.get('ImagesDeleted') or [])
        case 'containers':
            result = client.containers.prune()
            num_deleted = len(result.get('ContainersDeleted') or [])
        case 'volumes':
            result = client.volumes.prune(filters={'all': True})
            num_deleted = len(result.get('VolumesDeleted') or [])
        case 'networks':
            result = client.networks.prune()
            num_deleted = len(result.get('NetworksDeleted') or [])
        case 'caches':
            result = client.api.prune_builds()
            num_deleted = len(result.get('CachesDeleted') or [])
        case _:
            raise ValueError(f'Invalid argument: {what}')
    ui.notify(f'{num_deleted or 0} {what} deleted, {result.get("SpaceReclaimed", 0) / 2**30:.1f} GB reclaimed')
    docker_prune_preview.refresh()


@ui.refreshable
def docker_prune_preview() -> None:
    dangling_images, stopped_containers, unused_volumes, unused_networks = docker_prune_dry_run()
    with ui.card().tight().props('flat bordered'):
        with ui.card_section().classes('w-full bg-gray-100'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('Docker').classes('text-lg text-bold')
                ui.button(icon='refresh', on_click=docker_prune_preview.refresh).props('flat outline')
        with ui.card_section():
            with ui.grid(columns='auto auto auto').classes('items-center'):
                for count, label, key in [
                    (dangling_images, 'Dangling images', 'images'),
                    (stopped_containers, 'Stopped containers', 'containers'),
                    (unused_volumes, 'Unused volumes', 'volumes'),
                    (unused_networks, 'Unused networks', 'networks'),
                ]:
                    ui.label(f'{count}').classes('text-bold')
                    ui.label(label).classes('text-sm text-gray-500')
                    ui.button(icon='delete', on_click=lambda k=key: docker_prune(k), color='negative').props('flat')
        with ui.card_section():
            ui.button('Prune cache', color='negative', on_click=lambda: docker_prune('caches')).props('flat outline')