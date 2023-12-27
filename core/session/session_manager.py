from datetime import datetime, timedelta
import hashlib
from core.db.redis.session import get_redis, close_redis
from core.session.models import Session
from core.enum.session_status import SessionStatus

TIMEOUT = 1
SESSION_EXPIRATION = timedelta(minutes=TIMEOUT)


class SessionManager:
    def __init__(self):
        self.redis = get_redis()

    async def create(self, user_id: str) -> Session:
        session = self._create_session(user_id)
        return await self._save(session)

    def _create_session(self, user_id: str) -> Session:
        now = datetime.utcnow()
        issued_at = int((now - datetime.utcfromtimestamp(0)).total_seconds())
        expires_at = int(
            ((now + SESSION_EXPIRATION) - datetime.utcfromtimestamp(0)).total_seconds()
        )

        access_token = hashlib.sha1(
            f"{user_id}-{issued_at}-{expires_at}".encode()
        ).hexdigest()

        session = Session(
            user_id=user_id,
            access_token=access_token,
            issued_at=issued_at,
            expires_at=expires_at,
        )
        return session

    async def _save(self, session: Session) -> Session:
        await self._delete_by_access_token(session.access_token)

        async with self.redis.pipeline(transaction=True) as pipe:
            token_key = "session.token:%s" % session.access_token
            await pipe.set(token_key, session.model_dump_json())
            await pipe.expireat(token_key, session.expires_at)
            await pipe.execute()
        return session

    async def _delete_by_access_token(self, access_token: str):
        await self.redis.delete("session.token:%s" % access_token)

    async def verify_access_token(self, access_token: str) -> Session | SessionStatus:
        session_data = await self.redis.get("session.token:%s" % access_token)
        if session_data is None:
            return SessionStatus.NOT_EXIST

        session = Session.model_validate_json(session_data)
        if self._is_not_expired(session):
            return session
        else:
            await self.delete(session)
            return SessionStatus.EXPIRED

    def _is_not_expired(self, session: Session) -> bool:
        now = datetime.utcnow()
        current_timestamp = int((now - datetime.utcfromtimestamp(0)).total_seconds())
        return session.expires_at > current_timestamp

    async def delete(self, session: Session):
        await self._delete_by_access_token(session.access_token)

    async def close(self):
        await close_redis(self.redis)
