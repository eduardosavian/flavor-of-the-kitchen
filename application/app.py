from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session

import crud
import models
import schemas
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from database import engine, get_db
from exceptions import UserException, RecipeException, CommentException
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:9000",
    "http://localhost:6000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication
@app.post("/signup/", tags=["user"])
def create_user_signup(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        crud.create_user(db, user)
        return signJWT(user.email)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


@app.post("/login/", tags=["user"])
def user_login(user: schemas.UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    if crud.check_user(db, user):
        return signJWT(user.email)
    raise HTTPException(status_code=400, detail="WRONG_USER")


# User
# Create
@app.post("/user/create/", response_model=schemas.User, dependencies=[Depends(JWTBearer())])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Update
@app.put("/user/update/{user_id}/", response_model=schemas.User, dependencies=[Depends(JWTBearer())])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_user(db, user_id, user)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Delete
@app.delete("/user/delete/{user_id}/", dependencies=[Depends(JWTBearer())])
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_user_by_id(db, user_id)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Get email
@app.get("/user/email/{user_email}/", dependencies=[Depends(JWTBearer())])
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    try:
        return crud.get_user_by_email(db, user_email)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Get id
@app.get("/user/id/{user_id}/", dependencies=[Depends(JWTBearer())])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_user_by_id(db, user_id)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Get all
@app.get("/user/id/", response_model=schemas.PaginatedUser)
def get_all_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_users = crud.get_all_users(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_users}
    return response


# Recipe
# Create
@app.post("/recipe/create/", dependencies=[Depends(JWTBearer())], response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_recipe(db, recipe)
    except RecipeException as cie:
        raise HTTPException(**cie.__dict__)


# Update
@app.put("/recipe/update/{recipe_id}/", dependencies=[Depends(JWTBearer())], response_model=schemas.Recipe)
def update_recipe(recipe_id: int, recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.update_recipe(db, recipe_id, recipe)


# Delete
@app.delete("/recipe/delete/{recipe_id}/", dependencies=[Depends(JWTBearer())])
def delete_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_recipe_by_id(db, recipe_id)
    except RecipeException as cie:
        raise HTTPException(**cie.__dict__)


# Get title
@app.get("/recipe/title/{recipe_title}/", dependencies=[Depends(JWTBearer())])
def get_recipe_by_title(recipe_title: str, db: Session = Depends(get_db)):
    try:
        return crud.get_recipe_by_title(db, recipe_title)
    except RecipeException as cie:
        raise HTTPException(**cie.__dict__)


# Get id
@app.get("/recipe/id/{recipe_id}/", dependencies=[Depends(JWTBearer())])
def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_recipe_by_id(db, recipe_id)
    except RecipeException as cie:
        raise HTTPException(**cie.__dict__)


# Get all
@app.get("/recipe/id/", response_model=schemas.PaginatedRecipe)
def get_all_recipes(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_recipes = crud.get_all_recipes(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_recipes}
    return response


# Comment
# Create
@app.post("/comment/create/", dependencies=[Depends(JWTBearer())], response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_comment(db, comment)
    except CommentException as cie:
        raise HTTPException(**cie.__dict__)


# Update
@app.put("/comment/update/{comment_id}/", dependencies=[Depends(JWTBearer())], response_model=schemas.Comment)
def update_comment(comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.update_comment(db, comment_id, comment)


# Delete
@app.delete("/comment/delete/{comment_id}/", dependencies=[Depends(JWTBearer())])
def delete_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_comment_by_id(db, comment_id)
    except CommentException as cie:
        raise HTTPException(**cie.__dict__)


# Get title
@app.get("/comment/title/{comment_title}/", dependencies=[Depends(JWTBearer())])
def get_comment_by_title(comment_title: str, db: Session = Depends(get_db)):
    try:
        return crud.get_comment_by_title(db, comment_title)
    except CommentException as cie:
        raise HTTPException(**cie.__dict__)


# Get id
@app.get("/comment/id/{comment_id}/", dependencies=[Depends(JWTBearer())])
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_comment_by_id(db, comment_id)
    except UserException as cie:
        raise HTTPException(**cie.__dict__)


# Get all
@app.get("/comment/id/", dependencies=[Depends(JWTBearer())], response_model=schemas.PaginatedComment)
def get_all_comments(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_comments = crud.get_all_comments(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_comments}
    return response
