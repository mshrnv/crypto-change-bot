"""Wallet model"""
from __future__ import annotations
from typing import Annotated

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True)]
user_id_fk = Annotated[int, mapped_column(ForeignKey('users.id'))]


class Wallet(Base):
    """Wallet model class"""
    __tablename__ = "wallets"

    id: Mapped[int_pk]
    user_id: Mapped[user_id_fk]
    is_deposit: Mapped[bool]
    balance: Mapped[int]
    hex_address: Mapped[str]
    base58_address: Mapped[str]
    public_key: Mapped[str]
    private_key: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
