from datetime import timedelta
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
import settings
import logging
from api.models import Token
from db.session import get_db
from security import create_access_token
from actions.auth import authenticate_user

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        logging.warning("Incorrect email or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email, "user_id": user.user_id}, expires_delta=access_token_expires
    )
    logging.debug("%s new token expires on %s", user.user_id, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
