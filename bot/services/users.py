from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import select, insert, update
from sqlalchemy.sql import func

from bot.database.models import User, Transaction, Wallet

if TYPE_CHECKING:
    from aiogram.types import User
    from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(
        session: AsyncSession,
        user: User,
) -> None:
    """Add a new user to the database."""
    user_id: int = user.id
    first_name: str = user.first_name
    last_name: str | None = user.last_name
    username: str | None = user.username
    language_code: str | None = user.language_code

    new_user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
        balance=0,
        is_premium=False
    )

    session.add(new_user)
    await session.commit()


async def user_exists(session: AsyncSession, user_id: int) -> bool:
    """Checks if the user is in the database."""
    query = select(User.id).filter_by(id=user_id).limit(1)

    result = await session.execute(query)

    user = result.scalar_one_or_none()
    return bool(user)


async def get_user_balances(session: AsyncSession, user_id: int) -> Dict[Any]:
    """Returns user's balances"""

    balances = {
        'trading_balance': 0,
        'deposit_balance': 0,
        'withdraw_balance': 0,
        'summary_balance': 0
    }

    query = select(User.balance).filter_by(id=user_id).limit(1)
    result = await session.execute(query)
    balance = result.scalar_one_or_none()
    balances['trading_balance'] = balance if balance else 0

    query = select(func.sum(Wallet.balance)).filter_by(user_id=user_id, is_deposit=True).limit(1)
    result = await session.execute(query)
    balance = result.scalar_one_or_none()
    balances['deposit_balance'] = balance if balance else 0

    query = select(func.sum(Wallet.balance)).filter_by(user_id=user_id, is_deposit=False).limit(1)
    result = await session.execute(query)
    balance = result.scalar_one_or_none()
    balances['withdraw_balance'] = balance if balance else 0

    balances['summary_balance'] = balances['trading_balance'] + balances['deposit_balance'] + balances[
        'withdraw_balance']

    return balances


async def deposit(session: AsyncSession, user_id: int, amount: int, wallet: str) -> bool:
    """Returns user's balance"""
    query = insert(Transaction).values(
        user_id=user_id,
        amount=amount,
        wallet=wallet,
        is_deposit=True
    )
    result = await session.execute(query)

    query = update(User).where(User.id == user_id).values(balance=User.balance + amount)
    result = await session.execute(query)

    await session.commit()

    return True


async def withdraw(session: AsyncSession, user_id: int, amount: int, wallet: str) -> bool:
    """Returns user's balance"""
    query = insert(Transaction).values(
        user_id=user_id,
        amount=amount,
        wallet=wallet,
        is_deposit=False
    )
    result = await session.execute(query)

    query = update(User).where(User.id == user_id).values(balance=User.balance - amount)
    result = await session.execute(query)

    await session.commit()

    return True


async def change_notifications_status(session: AsyncSession, user_id: int) -> bool:
    """Changes user's notifications status"""

    query = select(User.notifications).filter_by(id=user_id).limit(1)
    result = await session.execute(query)
    notifications_status = result.scalar_one_or_none()

    query = update(User).where(User.id == user_id).values(notifications=not notifications_status)
    result = await session.execute(query)
    await session.commit()

    return not notifications_status


async def get_notifications_status(session: AsyncSession, user_id: int) -> bool:
    """Changes user's notifications status"""
    query = select(User.notifications).filter_by(id=user_id).limit(1)
    result = await session.execute(query)
    notifications_status = result.scalar_one_or_none()

    return notifications_status
