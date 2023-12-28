from core.config import AppConfig
from core.enum.session_status import SessionStatus
from core.session import JWTManager


def test_jwt():
    # load config
    _config = AppConfig().load_config("./test-config.toml")

    jwt_manager = JWTManager()
    access_token: str = jwt_manager.create_access_token(user_id="hwanee")

    user_id = jwt_manager.get_current_user(access_token)
    assert "hwanee" == user_id

    wrong_token = jwt_manager.get_current_user("testifinthere")
    assert wrong_token == SessionStatus.NOT_EXIST
