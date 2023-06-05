import time
from typing import Union
from db.dals import SensorDAL
from api.models import Sensor, SensorCreate, SensorIdRespose
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_new_sensor(
    controller_id: int, body: SensorCreate, session
) -> Union[Sensor, None]:
    async with session.begin():
        sensor_dal = SensorDAL(session)
        sensor = await sensor_dal.create_sensor(controller_id, body)
        return sensor


async def _get_sensor_by_id(id: int, session: AsyncSession) -> Union[Sensor, None]:
    async with session.begin():
        sensor_dal = SensorDAL(session)
        sensor = await sensor_dal.get_sensor_by_id(id=id)
        return sensor


async def _delete_sensor(
    id: int, session: AsyncSession
) -> Union[SensorIdRespose, None]:
    async with session.begin():
        sensor_dal = SensorDAL(session)
        deleted_sensor_id = await sensor_dal.delete_sensor(id)
        return SensorIdRespose(id=deleted_sensor_id)


async def _update_sensor(
    id: int, updated_sensor_params: dict, session: AsyncSession
) -> Union[SensorIdRespose, None]:
    async with session.begin():
        sensor_dal = SensorDAL(session)
        updated_sensor = await sensor_dal.update_sensor(
            sensor_id=id,
            last_changed=int(time.time()),
            **updated_sensor_params.dict(exclude_unset=True)
        )
        return SensorIdRespose(id=updated_sensor)
