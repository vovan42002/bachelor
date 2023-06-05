from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import logging
from actions.auth import get_current_user_from_token
from api.models import (
    UserCreate,
    ShowUser,
    DeleteUserResponse,
    UpdatedUserResponse,
    UpdatedUserRequest,
)
from db.models import User
from db.session import get_db
from actions.user import (
    _create_new_user,
    _delete_user,
    _update_user,
    _get_user_by_id,
    check_permission,
)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(
    body: UserCreate, session: AsyncSession = Depends(get_db)
) -> ShowUser:
    new_user = await _create_new_user(body, session)
    if new_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with email {body.email} already exists"
        )
    logging.info("Create new user with id: %s", new_user.user_id)
    return new_user


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    if not await check_permission(user_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id {current_user.user_id} cannot delete user with id {user_id}",
        )
    deleted_user_id = await _delete_user(user_id, session)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    logging.info("Delete user with id: %s", deleted_user_id)
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, session)
    if user is None:
        logging.warning("User with id %s not found", user_id)
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    logging.info("User with id %s found", user_id)
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: int,
    body: UpdatedUserRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    if not await check_permission(user_id, current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id {current_user.user_id} cannot update user with id {user_id}",
        )
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user = await _get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    updated_user_id = await _update_user(
        updated_user_params=body, session=session, user_id=user_id
    )
    logging.info("User with id: %s updated successfully", updated_user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)
