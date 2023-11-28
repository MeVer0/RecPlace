import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.auth.auth_backend import auth_backend, fastapi_users
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.models import User

from src.admin.router import router as admin_router
from src.user.router import router as user_router

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(admin_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app=app)
