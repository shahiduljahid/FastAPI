from fastapi import APIRouter
from typing import List
from fastapi import Depends, status
from blog import schemas
from blog import database
from sqlalchemy.orm import Session
from blog.repository import user

get_db = database.get_db
router = APIRouter(tags=["Users"], prefix="/user")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    req: schemas.User,
    db: Session = Depends(get_db),
):
    return user.create_user(req, db)


@router.get(
    "/",
    response_model=List[schemas.ShowUser],
    status_code=status.HTTP_200_OK,
)
def read_users(
    db: Session = Depends(get_db),
):
    return user.read_users(db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowUser)
def single_user(
    id: int,
    db: Session = Depends(get_db),
):
    return user.single_user(id, db)
