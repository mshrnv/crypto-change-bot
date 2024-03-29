"""User model"""
from __future__ import annotations

from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, created_at


class User(Base):
    """User model class"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    created_at: Mapped[created_at]
    balance: Mapped[int]
    notifications: Mapped[bool] = mapped_column(Boolean, default=False)
    is_premium: Mapped[bool]
