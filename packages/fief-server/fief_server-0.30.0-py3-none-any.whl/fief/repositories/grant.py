from pydantic import UUID4
from sqlalchemy import select

from fief.models import Grant
from fief.repositories.base import BaseRepository, UUIDRepositoryMixin


class GrantRepository(BaseRepository[Grant], UUIDRepositoryMixin[Grant]):
    model = Grant

    async def get_by_user_and_client(
        self, user_id: UUID4, client_id: UUID4
    ) -> Grant | None:
        statement = select(Grant).where(
            Grant.user_id == user_id, Grant.client_id == client_id
        )
        return await self.get_one_or_none(statement)
