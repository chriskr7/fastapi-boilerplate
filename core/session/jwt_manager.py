from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.enum.session_status import SessionStatus

SECRET_KEY = "ea5012810e1aa4aaccfb93b0216ac4ddc9bbdcd920f0545267fb5eb0c07ddb68"
ALGORITHM = "HS256"
TIMEOUT = 180
SESSION_EXPIRATION = timedelta(minutes=TIMEOUT)


class JWTManager:
    def create_access_token(self, user_id: str) -> str:
        now = datetime.utcnow()
        to_encode = {
            "user_id": user_id,
            "issued_at": int((now - datetime.utcfromtimestamp(0)).total_seconds()),
            "expires_at": int(
                (
                    (now + SESSION_EXPIRATION) - datetime.utcfromtimestamp(0)
                ).total_seconds()
            ),
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_current_user(self, access_token: str) -> str | SessionStatus:
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload["issued_at"])
            if (
                all(
                    payload_key in payload
                    for payload_key in ["user_id", "issued_at", "expires_at"]
                )
                is False
            ):
                return SessionStatus.NOT_VALID
        except JWTError:
            return SessionStatus.NOT_EXIST

        if self._is_not_expired(payload["expires_at"]):
            return payload["user_id"]
        else:
            return SessionStatus.EXPIRED

    def _is_not_expired(self, expires_at: int) -> bool:
        now = datetime.utcnow()
        current_timestamp = int((now - datetime.utcfromtimestamp(0)).total_seconds())
        return expires_at > current_timestamp
