import docker
import pytest

from air_link import main_page

pytest_plugins = ['nicegui.testing.user_plugin']


@pytest.fixture
def registered_main_page(monkeypatch: pytest.MonkeyPatch) -> None:
    """Register the main page with Docker unavailable, like on a machine without a Docker daemon."""
    def refuse_connection(*args, **kwargs) -> None:
        raise docker.errors.DockerException('no Docker daemon')

    monkeypatch.setattr(docker, 'DockerClient', refuse_connection)
    main_page.create_page()
