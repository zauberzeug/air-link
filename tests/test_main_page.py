from nicegui.testing import User


async def test_main_page_shows_all_sections(user: User, registered_main_page: None) -> None:
    await user.open('/')
    await user.should_see('Air Link')
    await user.should_see('Environment variables')
    await user.should_see('Packages')
    await user.should_see('System')
    await user.should_see('Disk space')
    await user.should_see('Docker')
    await user.should_see('Network')
