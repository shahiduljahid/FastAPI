from fastapi import HTTPException
from blog import schemas, models, hashing
from sqlalchemy.orm import Session


def create_user(req: schemas.User, db: Session):
    new_user = models.User(
        name=req.name, email=req.email, password=hashing.Hash.bcrypt(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def read_users(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users")
    return users


def single_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {id} not found")
    return user
