from http import HTTPStatus
from typing import Iterable

from fastapi import HTTPException, APIRouter
from fastapi_pagination import Page, paginate

from app.database import users
from app.models.User import User

from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=User)
async def user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user_data = users.get_user(user_id)
    if not user_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user_data


@router.get("/", status_code=HTTPStatus.OK, response_model=Page[User])
def users() -> Iterable[User]:
    return users.get_users() #paginate(users.get_users())
