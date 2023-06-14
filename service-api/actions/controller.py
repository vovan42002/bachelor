import time
from typing import List, Union
from db.dals import ControllerDAL, UserDAL
from api.models import Controller, ControllerCreate, ControllerIdRespose
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Sensor


async def _create_new_controller(
    body: ControllerCreate, session
) -> Union[Controller, None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        controller = await controller_dal.create_controller(body)
        return controller


async def _get_controller_by_id(
    id: int, session: AsyncSession
) -> Union[Controller, None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        controller = await controller_dal.get_controller_by_id(id=id)
        return controller


async def _get_controller_by_email(
    email: str, session: AsyncSession
) -> Union[ControllerIdRespose, None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email=email)
        if user is not None:
            controller = await controller_dal.get_controller_by_user_id(
                user_id=user.user_id
            )
            if controller is not None:
                return ControllerIdRespose(id=controller.id)
            return None
        return None


async def _get_sensors(id: int, session: AsyncSession) -> Union[List[Sensor], None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        sensors = await controller_dal.get_sensors(id=id)
        return sensors


async def _delete_controller(
    id: int, session: AsyncSession
) -> Union[ControllerIdRespose, None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        deleted_controller_id = await controller_dal.delete_controller(id)
        return ControllerIdRespose(id=deleted_controller_id)


async def _update_controller(
    id: int, updated_controller_params: dict, session: AsyncSession
) -> Union[ControllerIdRespose, None]:
    async with session.begin():
        controller_dal = ControllerDAL(session)
        updated_controller = await controller_dal.update_controller(
            controller_id=id,
            last_changed=int(time.time()),
            **updated_controller_params.dict(exclude_unset=True)
        )
        return ControllerIdRespose(id=updated_controller)
