import datetime
import uuid

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        Numeric, String)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

# Local import
from app.database.configuration import Base

#Base is where we start the database

class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True, nullable=False)
    #date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_added = Column(String, nullable=False)
    name = Column(String, nullable=False)
    chef_name = Column(String, nullable=False)
    '''
    food_category = Column(String, nullable=False)
    menu_name = Column(String, nullable=False)
    food_category = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    address = Column(String, nullable=False)
    podcast_file_path = Column(String, nullable=False)
    video_file_path = Column(String, nullable=False)
    card_photo_file_path = Column(String, nullable=False)
    podcast_file_path = Column(String, nullable=False)
    menu_list_photo_file_path = Column(String, nullable=False)
    podcast_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    other_item_name = Column(String, nullable=False)
    podcast_file_path = Column(String, nullable=False)
    '''
