from asyncio.log import logger
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from schemas import ShipmentsModel, UserModel


def get_shipment(shipment_id: int) -> ShipmentsModel | None:
    shipment = session.scalar(select(ShipmentsModel).where(ShipmentsModel.id == shipment_id))
    return shipment


def create_shipment(data: dict) -> ShipmentsModel | None:
    creating_shipment = ShipmentsModel(**data)

    session.add(creating_shipment)

    try:
        session.commit()
        return creating_shipment
    except IntegrityError:
        session.rollback()
        logger.exception("Failed to create shipment!")
        return None


def update_shipment(id: int, updates: dict) -> bool:
    session.query(ShipmentsModel).filter(ShipmentsModel.id == id).update(updates)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def get_user_by_shipment(id: int) -> UserModel | None:
    shipment = session.scalar(select(ShipmentsModel).where(ShipmentsModel.id == id))
    if shipment is None:
        return None
    return shipment.user



