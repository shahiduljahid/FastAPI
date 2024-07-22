from typing import List
from fastapi import Depends, status, APIRouter
from blog import schemas
from blog import database
from sqlalchemy.orm import Session
from blog.repository import blog
from blog import OAuth2

get_db = database.get_db

router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.get(
    "/",
    response_model=List[schemas.ShowUserBlog],
    status_code=status.HTTP_200_OK,
)
def read_items(
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return blog.read_items(db)


@router.get(
    "/{id}",
    status_code=200,
    response_model=schemas.ShowUserBlog,
)
def single_item(
    id: int,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return blog.single_item(id, db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create(
    req: schemas.Blog,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return blog.create(req, db)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    id: int,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):

    return blog.delete_item(id, db)


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_item(
    id: int,
    req: schemas.Blog,
    current_user: schemas.User = Depends(OAuth2.get_current_user),
    db: Session = Depends(get_db),
):
    return blog.update_item(id, req, db)
