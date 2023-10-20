import datetime
import uuid
from sqlalchemy import (Column,  DateTime, String, Boolean, Enum, ForeignKey, Integer, Time)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, validates
from app.enums import search_enums
from app.func import geo_location
# Local import
from app.database.configuration import Base


    

class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, nullable=False)
    menu = Column(String, nullable=False)
    instagram = Column(String, nullable=False)
    chef_name = Column(String, nullable=False)
    cuisine = Column(Enum(search_enums.CuisineEnum), nullable=False)
    establishment_type = Column(Enum(search_enums.EstablishmentTypeEnum), nullable=False)
    address = Column(String, nullable=False)
    lat = Column(String) 
    lon = Column(String)

    @validates('address')
    def _validate_address(self, key, address):
        # Compute lat and lon from the address
        lat, lon = geo_location.extract_lat_long_via_address(address)
        print(lat)
        # Set the lat and lon fields
        self.lat = lat
        self.lon = lon

        return address
    
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    open_now = Column(Enum(search_enums.OpenNowEnum), nullable=False)
    
    opening_hours = relationship("OpeningHours", back_populates="restaurant")
    dishes = relationship("Dish", back_populates="restaurant")

class OpeningHours(Base):
    __tablename__ = 'opening_hours'

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    day_of_week = Column(Enum(search_enums.DayOfWeekEnum), nullable=False)  # e.g., 'Monday', 'Tuesday', ...
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    restaurant_id = Column(String, ForeignKey('restaurant.id'))

    # Create a relationship with the Business model if needed
    restaurant = relationship("Restaurant", back_populates="opening_hours")

class Dish(Base):
    __tablename__ = "dishes"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    date_added = Column(DateTime, default=datetime)
    menu_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    diet = Column(Enum(search_enums.DietEnum), nullable=False)
    food_type = Column(Enum(search_enums.FoodTypeEnum), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    restaurant_id = Column(String, ForeignKey("restaurant.id"))
    
    # Relationship with the Restaurant model
    restaurant = relationship("Restaurant", back_populates="dishes")
    other_items = relationship("OtherItem", back_populates="dish")

class OtherItem(Base):
    __tablename__ = "other_items"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    dish_id = Column(String, ForeignKey("dishes.id"))

    # Relationship with the Dish model
    dish = relationship("Dish", back_populates="other_items")
    
    #content = relationship("Content", back_populates="dish_content")

'''
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
