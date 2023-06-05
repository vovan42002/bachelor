from typing import Union, List
from sqlalchemy import update, delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import time

from db.models import User, Sensor, Controller


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, email: str, hashed_password: str) -> Union[User, None]:
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a user: {str(e)}")
            return None

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


class ControllerDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_controller(self, body: Controller) -> Union[Controller, None]:
        try:
            new_controller = Controller(
                user_id=body.user_id,
                last_changed=int(time.time()),
                force_enable=body.force_enable,
                status=body.status,
                repeat=body.repeat,
                start_time=-1,
                end_time=-1,
            )
            self.db_session.add(new_controller)
            await self.db_session.flush()
            return new_controller
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a controller: {str(e)}")
            return None

    async def get_controller_by_id(self, id: int) -> Union[Controller, None]:
        query = select(Controller).where(Controller.id == id)
        res = await self.db_session.execute(query)
        controller_row = res.fetchone()
        if controller_row is not None:
            return controller_row[0]
        return None

    async def get_controller_by_email(self, email: str) -> Union[Controller, None]:
        query = select(Controller).where(User.email == email)
        res = await self.db_session.execute(query)
        controller_row = res.fetchone()
        if controller_row is not None:
            return controller_row[0]

    async def get_sensors(self, id: int) -> Union[List[Sensor], None]:
        query = select(Sensor).where(Controller.id == id)
        res = await self.db_session.execute(query)
        sensors = res.fetchall()
        if sensors is not None:
            return sensors

    async def delete_controller(self, id: int) -> Union[int, None]:
        query = delete(Controller).where(Controller.id == id).returning(Controller.id)
        res = await self.db_session.execute(query)
        controller_row = res.fetchone()
        if controller_row is not None:
            return controller_row[0]

    async def update_controller(self, controller_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(Controller)
            .where(and_(Controller.id == controller_id))
            .values(kwargs)
            .returning(Controller.id)
        )
        res = await self.db_session.execute(query)
        update_controller_id_row = res.fetchone()
        if update_controller_id_row is not None:
            return update_controller_id_row[0]


class SensorDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_sensor(
        self, controller_id: int, body: Sensor
    ) -> Union[Sensor, None]:
        try:
            new_sensor = Sensor(
                type=body.type,
                actual=-1,
                expected=-1,
                last_changed=int(time.time()),
                controller_id=controller_id,
            )
            self.db_session.add(new_sensor)
            await self.db_session.flush()
            return new_sensor
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a sensor: {str(e)}")
            return None

    async def get_sensor_by_id(self, id: int) -> Union[Sensor, None]:
        query = select(Sensor).where(Sensor.id == id)
        res = await self.db_session.execute(query)
        sensor_row = res.fetchone()
        if sensor_row is not None:
            return sensor_row[0]

    async def delete_sensor(self, id: int) -> Union[int, None]:
        query = delete(Sensor).where(Sensor.id == id).returning(Sensor.id)
        res = await self.db_session.execute(query)
        sensor_row = res.fetchone()
        if sensor_row is not None:
            return sensor_row[0]

    async def update_sensor(self, sensor_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(Sensor)
            .where(and_(Sensor.id == sensor_id))
            .values(kwargs)
            .returning(Sensor.id)
        )
        res = await self.db_session.execute(query)
        update_sensor_id_row = res.fetchone()
        if update_sensor_id_row is not None:
            return update_sensor_id_row[0]
