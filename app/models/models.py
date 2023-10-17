import datetime
import uuid
from sqlalchemy import (Column,  DateTime, Integer, String, Boolean, ForeignKey, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

# Local import
from app.database.configuration import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)

    name = Column(String, nullable=False)
    chef_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)

    #featured = relationship("Dish", back_populates="restaurant")
'''
class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)
    date_added = Column(DateTime, default=datetime.date)
    menu_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    other_items = Column(String, nullable=False)
    is_active = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))

    restaurant = relationship("Restaurant", back_populates="featured")
    content = relationship("Content", back_populates="dish_content")

class Content(Base):
    __tablename__ = "content_dish"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)
    podcast_name = Column(String, nullable=True)
    content_id = Column(Integer, ForeignKey("dishes.id"))

    dish_content = relationship("Dish", back_populates="content")


     podcast_file_path = Column(String, nullable=False)
    video_file_path = Column(String, nullable=False)
    card_photo_file_path = Column(String, nullable=False)
    podcast_file_path = Column(String, nullable=False)
    menu_list_photo_file_path = Column(String, nullable=False)
    other_item_name = Column(String, nullable=False)
    '''