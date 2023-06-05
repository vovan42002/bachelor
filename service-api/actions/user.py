from typing import Union
from uuid import UUID

from api.models import UserCreate, ShowUser
from db.dals import UserDAL
from hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                email=user.email,
                is_active=user.is_active,
            )


async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user = await user_dal.delete_user(user_id=user_id)
        return deleted_user


async def _update_user(updated_user_params: dict, user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user = await user_dal.update_user(user_id, **updated_user_params.dict())
        return updated_user


async def _get_user_by_id(user_id, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                email=user.email,
                is_active=user.is_active,
            )


async def check_permission(target_user_id: UUID, current_user_id: UUID) -> bool:
    return target_user_id == current_user_id
