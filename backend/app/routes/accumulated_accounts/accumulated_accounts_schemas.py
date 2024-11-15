from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AccumulatedAccountSchema:
    session: AsyncSession
    owner_id: int
    user_id: int
    account_id: int
    permissions_list: list
