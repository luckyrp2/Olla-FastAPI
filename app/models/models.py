import datetime
import uuid

from sqlalchemy import (Column,  DateTime, Integer, String, ForeignKey)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

# Local import
from app.database.configuration import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    chef_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    podcast_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(String, nullable=False)

    featured = relationship("Dish", back_populates="restaurant")

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, nullable=False) 
    date_added = Column(DateTime, default=datetime.date)
    menu_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    other_items = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))

    restaurant = relationship("Restaurant", back_populates="featured")
    content = relationship("Content", back_populates="dish_content")

class Content(Base):
    __tablename__ = "content_dish"

    podcast_name = Column(String, nullable=True)
    content_id = Column(Integer, ForeignKey("dishes.id"))

    dish_content = relationship("Dish", back_populates="content")


    '''
    podcast_file_path = Column(String, nullable=False)
    video_file_path = Column(String, nullable=False)
    card_photo_file_path = Column(String, nullable=False)
    podcast_file_path = Column(String, nullable=False)
    menu_list_photo_file_path = Column(String, nullable=False)
    other_item_name = Column(String, nullable=False)
    '''