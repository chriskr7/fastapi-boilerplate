import pytest

from core.config import AppConfig
from core.enum.session_status import SessionStatus
from core.session import Session, SessionManager


@pytest.mark.asyncio
async def test_session():
    # load config
    _config = AppConfig().load_config("./test-config.toml")

    session_manager = SessionManager()
    session: Session = await session_manager.create("hwanee")

    got_session = await session_manager.verify_access_token(session.access_token)
    assert session == got_session

    wrong_session = await session_manager.verify_access_token("testifinthere")
    assert wrong_session == SessionStatus.NOT_EXIST
