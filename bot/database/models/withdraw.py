"""Withdraw model"""
from __future__ import annotations
from typing import Annotated

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True)]
user_id_fk = Annotated[int, mapped_column(ForeignKey('users.id'))]


class Withdraw(Base):
    """Withdraw model class"""
    __tablename__ = "withdraws"

    id: Mapped[int_pk]
    user_id: Mapped[user_id_fk]
    from_address: Mapped[str]
    to_address: Mapped[str]
    amount: Mapped[float]
    transaction_id: Mapped[str]
