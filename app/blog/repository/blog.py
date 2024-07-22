from fastapi import HTTPException
from blog import schemas, models
from sqlalchemy.orm import Session


def read_items(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def single_item(id: int, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    return blog


def create(req: schemas.Blog, db):
    new_blog = models.Blog(
        title=req.title, body=req.body, published=req.published, user_id=3
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_item(
    id: int,
    db,
):
    item = db.query(models.Blog).filter(models.Blog.id == id)
    if item.first():
        item.delete(synchronize_session=False)
    else:
        raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    db.commit()
    return "Deleted"


def update_item(id: int, req: schemas.Blog, db):
    blog_item = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_item:
        raise HTTPException(status_code=404, detail=f"Blog with {id} not found")
    # Update the blog post fields
    for key, value in req.model_dump().items():
        setattr(blog_item, key, value)
    db.commit()
    db.refresh(blog_item)
    return blog_item
