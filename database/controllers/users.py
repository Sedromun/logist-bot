from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from schemas.users import RoleModel, UserModel


def get_user(user_id: int) -> UserModel | None:
    user = session.scalar(select(UserModel).where(UserModel.id == user_id))
    return user


def check_role(user_id: int, role: str) -> bool:
    user = get_user(user_id=user_id)
    return user.role.role_name == role


def register_user(tg_id: int) -> UserModel | None:
    creating_user = UserModel(id=tg_id)

    session.add(creating_user)

    try:
        session.commit()
        return creating_user
    except IntegrityError:
        session.rollback()
        return None


def update_user(tg_id: int, updates: dict) -> bool:
    session.query(UserModel).filter(UserModel.id == tg_id).update(updates)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def get_user_by_city(city: str) -> UserModel | None:
    role = session.scalar(select(RoleModel).where(RoleModel.city == city))
    if role is None:
        return None
    return role.user


