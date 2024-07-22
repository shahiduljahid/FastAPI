from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas, token_1
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=200)
def login(
    req: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(database.get_db),
):

    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    if not Hash.verify(req.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")

    access_token = token_1.create_access_token(data={"sub": user.email})

    return schemas.Token(access_token=access_token, token_type="bearer")
