from __future__ import annotations

from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, created_at

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=True)]
user_id_ref = Annotated[int, mapped_column()]


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int_pk]
    user_id: Mapped["User"] = relationship()
    wallet: Mapped[str]
    amount: Mapped[int]
    is_deposit: Mapped[bool]
    created_at: Mapped[created_at]
