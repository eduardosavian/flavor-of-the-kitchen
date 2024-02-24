from typing import List
from pydantic import BaseModel


# Comment
class CommentBase(BaseModel):
    title: str
    description: str
    recipe_id: str
    user_id: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedComment(BaseModel):
    limit: int
    offset: int
    data: List[Comment]


# Recipe
class RecipeBase(BaseModel):
    title: str
    description: str
    contents: str
    user_id: str


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True


class PaginatedRecipe(BaseModel):
    limit: int
    offset: int
    data: List[Recipe]


# User
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    recipes: List[Recipe] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True


class PaginatedUser(BaseModel):
    limit: int
    offset: int
    data: List[User]


# Login
class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "x@x.com",
                "password": "pass"
            }
        }
