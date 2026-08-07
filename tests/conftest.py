import pytest

from air_link import main_page, system

pytest_plugins = ['nicegui.testing.user_plugin']


@pytest.fixture
def registered_main_page(monkeypatch: pytest.MonkeyPatch) -> None:
    """Register the main page with Docker unavailable, like on a machine without a Docker daemon."""
    monkeypatch.setattr(system, '_get_docker_client', lambda: None)
    main_page.create_page()
