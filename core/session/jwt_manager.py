from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.enum.session_status import SessionStatus
from core.enum.token_type import TokenType

SECRET_KEY = "ea5012810e1aa4aaccfb93b0216ac4ddc9bbdcd920f0545267fb5eb0c07ddb68"
ALGORITHM = "HS256"
TIMEOUT = 180
SESSION_EXPIRATION = timedelta(minutes=TIMEOUT)


class JWTManager:
    def create_access_token(
        self, sub: str, token_type: TokenType = TokenType.ACCESS
    ) -> str:
        now = datetime.utcnow()
        to_encode = {
            "sub": sub,
            "iat": int((now - datetime.utcfromtimestamp(0)).total_seconds()),
            "exp": int(
                (
                    (now + SESSION_EXPIRATION) - datetime.utcfromtimestamp(0)
                ).total_seconds()
            ),
            "type": token_type.value,
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user(self, access_token: str) -> str | SessionStatus:
        try:
            payload = jwt.decode(
                access_token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"require_sub": True, "require_exp": True},
            )
        except JWTError:
            return SessionStatus.NOT_VALID

        if self._is_not_expired(payload["exp"]):
            return payload["sub"]
        else:
            return SessionStatus.EXPIRED

    def _is_not_expired(self, exp: int) -> bool:
        now = datetime.utcnow()
        current_timestamp = int((now - datetime.utcfromtimestamp(0)).total_seconds())
        return exp > current_timestamp
