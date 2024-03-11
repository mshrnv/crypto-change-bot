from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, created_at, int_pk


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    created_at: Mapped[created_at]
    balance: Mapped[int]
    is_premium: Mapped[bool]
