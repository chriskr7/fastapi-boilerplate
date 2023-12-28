import pytest

from core.config import AppConfig
from core.enum.session_status import SessionStatus
from core.session import SessionManager


@pytest.mark.asyncio
async def test_session():
    # load config
    _config = AppConfig().load_config("./test-config.toml")

    session_manager = SessionManager()
    access_token: str = await session_manager.create_access_token(user_id="hwanee")

    user_id = await session_manager.get_current_user(access_token)
    assert "hwanee" == user_id

    wrong_session = await session_manager.get_current_user("testifinthere")
    assert wrong_session == SessionStatus.NOT_EXIST
