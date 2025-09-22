from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from schemas.users import RoleModel
from asyncio.log import logger



def create_role() -> RoleModel | None:
    creating_role = RoleModel()
    print(create_role)
    session.add(creating_role)

    try:
        session.commit()
        return creating_role
    except IntegrityError as e:
        session.rollback()
        logger.exception("Failed to create role!" + str(e))
        return None

def update_role(id: int, updates: dict) -> bool:
    session.query(RoleModel).filter(RoleModel.id == id).update(updates)
    try:
        session.commit()
        logger.info("Role '" + str(id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        logger.exception(
            f"Integrity error in update_role '{str(id)}' - can't commit in db",
            exc_info=e,
        )
        return False


def get_role(role_id: int) -> RoleModel | None:
    role = session.scalar(select(RoleModel).where(RoleModel.id == role_id))
    return role
