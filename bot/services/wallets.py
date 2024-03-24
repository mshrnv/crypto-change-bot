from __future__ import annotations
from typing import TYPE_CHECKING, List, Any

from sqlalchemy import select, insert, update

from bot.database.models import Wallet, User

if TYPE_CHECKING:
    from aiogram.types import User
    from sqlalchemy.ext.asyncio import AsyncSession


async def add_wallet(
        session: AsyncSession,
        user_id: int,
        is_deposit: bool,
        wallet
) -> None:
    """Add a new user deposit wallet to the database"""
    new_wallet = Wallet(
        user_id=user_id,
        is_deposit=is_deposit,
        balance=0,
        hex_address=wallet['hex_address'],
        base58_address=wallet['base58check_address'],
        public_key=wallet['public_key'],
        private_key=wallet['private_key'],
    )

    session.add(new_wallet)
    await session.commit()


async def get_user_wallets(
        session: AsyncSession,
        user_id: int,
        is_deposit: bool
) -> List[Any]:
    query = select(Wallet).filter_by(user_id=user_id, is_deposit=is_deposit, is_deleted=False)
    result = await session.execute(query)

    wallets = result.fetchall()
    return wallets


async def get_wallet_info(
        session: AsyncSession,
        wallet_id: int,
) -> List[Any]:
    query = select(Wallet).filter_by(id=wallet_id).limit(1)
    result = await session.execute(query)

    wallet_info = result.scalar_one_or_none()
    return wallet_info


async def delete_wallet(
        session: AsyncSession,
        wallet_id: int
) -> bool:
    query = update(Wallet).where(Wallet.id == wallet_id).values(is_deleted=True)
    await session.execute(query)
    await session.commit()

    return True


async def get_trading_wallet_balance(
        session: AsyncSession,
        user_id: int
) -> int:
    query = select(User.balance).filter_by(id=user_id).limit(1)
    result = await session.execute(query)

    balance = result.scalar_one_or_none()
    return balance
