"""Transfer model"""
from __future__ import annotations
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from bot.database.models.base import created_at

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True)]
user_id_fk = Annotated[int, mapped_column(ForeignKey('users.id'))]


class Transfer(Base):
    """Transfer to trading wallet model class"""
    __tablename__ = "transfers"

    id: Mapped[int_pk]
    user_id: Mapped[user_id_fk]
    from_wallet_id: Mapped[int]
    amount: Mapped[float]
    created_at: Mapped[created_at]
