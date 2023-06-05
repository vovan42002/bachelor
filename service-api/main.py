from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.user_handlers import user_router
from api.login_handlers import login_router
from api.controller_handlers import controller_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="server")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(
    controller_router, prefix="/controller", tags=["controller"]
)
app.include_router(main_api_router)
