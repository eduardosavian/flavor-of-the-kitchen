from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

    recipes = relationship("Recipe", back_populates="user_recipe")
    comments = relationship("Comment", back_populates="user_comment")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    contents = Column(String(255))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_recipe = relationship("User", back_populates="recipes")
    
    comments = relationship("Comment", back_populates="recipe_comment")
    
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    recipe_comment = relationship("Recipe", back_populates="comments") 

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_comment = relationship("User", back_populates="comments")
