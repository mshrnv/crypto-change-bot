"""Transaction model"""
from __future__ import annotations
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True)]
user_id_fk = Annotated[int, mapped_column(ForeignKey('users.id'))]


class Transaction(Base):
    """Transaction model class"""
    __tablename__ = "transactions"

    id: Mapped[int_pk]
    user_id: Mapped[user_id_fk]
    wallet: Mapped[str]
    amount: Mapped[int]
    is_deposit: Mapped[bool]
    created_at: Mapped[created_at]
