from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from actions.auth import get_current_user_from_token
from actions.controller import (
    _create_new_controller,
    _get_controller_by_email,
    _get_controller_by_id,
    _delete_controller,
    _get_sensors,
    _update_controller,
)
from actions.sensor import (
    _create_new_sensor,
    _delete_sensor,
    _get_sensor_by_id,
    _update_sensor,
)
from api.models import (
    Controller,
    ControllerUpdate,
    ControllerCreate,
    ControllerIdRespose,
    Sensor,
    SensorCreate,
    SensorIdRespose,
    SensorUpdate,
)
from db.models import User
from db.session import get_db

controller_router = APIRouter()


@controller_router.post("/")
async def create_controller(
    body: ControllerCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> Controller:
    new_controller = await _create_new_controller(body, session)
    if new_controller is None:
        raise HTTPException(status_code=404, detail=f"Some error")
    return new_controller


@controller_router.get("/")
async def get_controller_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> Controller:
    controller = await _get_controller_by_id(id=id, session=session)
    if controller is None:
        raise (
            HTTPException(status_code=404, detail=f"Controller with id {id} not found")
        )
    return controller


@controller_router.get("/email", response_model=ControllerIdRespose)
async def get_controller_by_email(
    email: str,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ControllerIdRespose:
    controller_id = await _get_controller_by_email(email=email, session=session)
    if controller_id is None:
        raise (
            HTTPException(
                status_code=404, detail=f"Controller with email {email} not found"
            )
        )
    return controller_id


@controller_router.get("/sensors")
async def get_sensors(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> List[Sensor]:
    sensors = await _get_sensors(id=id, session=session)
    if sensors is None:
        raise (HTTPException(status_code=404, detail=f"Sensors not found"))
    return sensors


@controller_router.delete("/")
async def delete_controller(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ControllerIdRespose:
    controller = await _delete_controller(id=id, session=session)
    if controller is None:
        raise (
            HTTPException(status_code=404, detail=f"Controller with id {id} not found")
        )
    return controller


@controller_router.patch("/")
async def update_controller(
    id: int,
    body: ControllerUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ControllerIdRespose:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    controller = await _get_controller_by_id(id=id, session=session)
    if controller is None:
        raise HTTPException(
            status_code=404, detail=f"Controller with id {id} not found"
        )
    updated_controller_id = await _update_controller(
        updated_controller_params=body, session=session, id=id
    )
    return updated_controller_id


@controller_router.post("/sensor")
async def create_sensor(
    controller_id: int,
    body: SensorCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> Sensor:
    new_sensor = await _create_new_sensor(controller_id, body, session)
    if new_sensor is None:
        raise HTTPException(
            status_code=404, detail="Can't create new sensor. Error during creating"
        )
    return new_sensor


@controller_router.get("/sensor")
async def get_sensor_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> Sensor:
    sensor = await _get_sensor_by_id(id=id, session=session)
    if sensor is None:
        raise (HTTPException(status_code=404, detail=f"Sensor with id {id} not found"))
    return sensor


@controller_router.delete("/sensor")
async def delete_sensor(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> SensorIdRespose:
    sensor = await _delete_sensor(id=id, session=session)
    if sensor is None:
        raise (HTTPException(status_code=404, detail=f"Sensor with id {id} not found"))
    return sensor


@controller_router.patch("/sensor")
async def update_sensor(
    id: int,
    body: SensorUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> SensorIdRespose:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    sensor = await _get_sensor_by_id(id=id, session=session)
    if sensor is None:
        raise HTTPException(status_code=404, detail=f"Sensor with id {id} not found")
    updated_sensor_id = await _update_sensor(
        updated_sensor_params=body, session=session, id=id
    )
    return updated_sensor_id
