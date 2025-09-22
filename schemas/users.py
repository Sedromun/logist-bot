from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, default=-1
    )
    role: Mapped["RoleModel"] = relationship(back_populates="user")
    shipments: Mapped[list["ShipmentsModel"]] = relationship(back_populates="user")



class RoleModel(BaseModel):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, index=True, autoincrement=True
    )
    code: Mapped[str] = mapped_column(nullable=True)
    role_name: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id), nullable=True)
    user: Mapped["UserModel"] = relationship(back_populates="role")

