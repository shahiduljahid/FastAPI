from fastapi import APIRouter
from typing import List
from fastapi import Depends, status
from .. import schemas
from .. import database
from sqlalchemy.orm import Session
from ..repository import user
from .. import OAuth2

get_db = database.get_db
router = APIRouter(tags=["Users"], prefix="/user")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    req: schemas.User,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return user.create_user(req, db)


@router.get(
    "/",
    response_model=List[schemas.ShowUser],
    status_code=status.HTTP_200_OK,
)
def read_users(
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return user.read_users(db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowUser)
def single_user(
    id: int,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return user.single_user(id, db)
