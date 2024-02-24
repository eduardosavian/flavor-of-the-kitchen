from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi import HTTPException

import models
import schemas


def check_user(db: Session, user: schemas.UserLoginSchema):
    db_user = db.query(models.User).filter(
        and_(models.User.email == user.email, models.User.password == user.password)).first()
    if db_user is None:
        return False
    return True


# User
def create_user(db: Session, user: schemas.UserCreate):
    db_user = get_user_by_email(db, user.email)
    if db_user is not None:
        raise HTTPException(status_code=406, detail="User already exists")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user_by_email(db, user.email)
    if db_user is not None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = get_user_by_id(db, user_id)
    db_user.name = user.name
    db_user.email = user.email
    if user.password != "":
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int):
    if db.query(models.User).get(user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = get_user_by_id(db, user_id)
    db.query(models.Recipe).filter(models.Recipe.user_id == user_id).delete()
    db.query(models.Comment).filter(models.Comment.user_id == user_id).delete()
    db.delete(db_user)
    db.commit()
    return


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_user_by_id(db: Session, user_id: int):
    if db.query(models.User).get(user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.User).get(user_id)


def get_all_users(db: Session, offset: int, limit: int):
    if db.query(models.User).offset(offset).limit(limit).all() is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.User).offset(offset).limit(limit).all()


# Recipe
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    get_user_by_id(db, int(recipe.user_id))
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeCreate):
    db_recipe = get_recipe_by_id(db, recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe = get_recipe_by_id(db, recipe_id)
    db_recipe.title = recipe.title
    db_recipe.description = recipe.description
    db_recipe.contents = recipe.contents
    db_recipe.user_id = recipe.user_id
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe_by_id(db: Session, recipe_id: int):
    if db.query(models.Recipe).get(recipe_id) is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe = get_recipe_by_id(db, recipe_id)
    db.query(models.Comment).filter(models.Comment.recipe_id == recipe_id).delete()
    db.delete(db_recipe)
    db.commit()
    return


def get_recipe_by_title(db: Session, recipe_title: str):
    if db.query(models.Recipe).get(recipe_title) is not None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db.query(models.Recipe).filter(models.Recipe.title == recipe_title).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    if db.query(models.Recipe).get(recipe_id) is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db.query(models.Recipe).get(recipe_id)
    #return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def get_all_recipes(db: Session, offset: int, limit: int):
    return db.query(models.Recipe).offset(offset).limit(limit).all()


# Comment
def create_comment(db: Session, comment: schemas.CommentCreate):
    get_recipe_by_id(db, int(comment.recipe_id))
    get_user_by_id(db, int(comment.user_id))
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = get_comment_by_id(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment = get_comment_by_id(db, comment_id)
    db_comment.title = comment.title
    db_comment.description = comment.description
    db_comment.recipe_id = comment.recipe_id
    db_comment.user_id = comment.user_id
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment_by_id(db: Session, comment_id: int):
    if db.query(models.Comment).get(comment_id) is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment = get_comment_by_id(db, comment_id)
    db.delete(db_comment)
    db.commit()
    return


def get_comment_by_title(db: Session, comment_title: str):
    if db.query(models.Comment).filter(models.Comment.title == comment_title).first() is not None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db.query(models.Comment).filter(models.Comment.title == comment_title).all()


def get_comment_by_id(db: Session, comment_id: int):
    if db.query(models.Comment).get(comment_id) is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_all_comments(db: Session, offset: int, limit: int):
    return db.query(models.Comment).offset(offset).limit(limit).all()
