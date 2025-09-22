from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from .base import BaseModel
from .users import UserModel

class ShipmentsModel(BaseModel):
    __tablename__ = "shipments"
    id: Mapped[int] = mapped_column(
        BigInteger, autoincrement=True, primary_key=True, unique=True, index=True
    )
    city: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True, default="pending")  # pending, accepted, rejected
    user: Mapped["UserModel"] = relationship(back_populates="shipments")
    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id), nullable=True)
    admin_id: Mapped[int] = mapped_column(nullable=False)
