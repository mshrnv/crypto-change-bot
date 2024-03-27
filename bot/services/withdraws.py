"""Withdraws service"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Withdraw


async def add_withdraw_transaction(
        session: AsyncSession,
        user_id: int,
        from_address: str,
        to_address: str,
        amount: float,
        transaction_id: str
) -> None:
    """Add a new withdraw-transaction to the database"""

    new_withdraw = Withdraw(
        user_id=user_id,
        from_address=from_address,
        to_address=to_address,
        amount=amount,
        transaction_id=transaction_id
    )

    session.add(new_withdraw)
    await session.commit()

    return new_withdraw


async def get_withdraw_history(
        session: AsyncSession,
        user_id: int
):
    """Returns all withdraw history list"""
    query = select(Withdraw.transaction_id).filter_by(user_id=user_id)
    result = await session.execute(query)

    history = result.fetchall()
    return history
