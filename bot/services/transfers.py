"""Withdraws service"""
from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Transfer, Wallet


async def add_transfer_transaction(
        session: AsyncSession,
        user_id: int,
        from_wallet_id: str,
        amount: float,
):
    """Add a new transfer-transaction to the database"""

    new_transfer = Transfer(
        user_id=user_id,
        from_wallet_id=from_wallet_id,
        amount=amount
    )
    session.add(new_transfer)

    query = update(Wallet).where(Wallet.id == from_wallet_id).values(balance=Wallet.balance + amount)
    await session.execute(query)

    await session.commit()
    return new_transfer


async def get_transfer_history(
        session: AsyncSession,
        user_id: int
):
    """Returns all transfer history list"""
    query = select(Transfer).filter_by(user_id=user_id)
    result = await session.execute(query)

    history = result.fetchall()
    return history
