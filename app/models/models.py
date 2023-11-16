import datetime
import uuid
from sqlalchemy import (Column,  JSON, DateTime, String, Boolean, Enum, ForeignKey, Integer, Time, Float)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, validates
from app.enums import search_enums
from app.func import geo_location
# Local import
from app.database.configuration import Base


class APIKey(Base):
    __tablename__ = "api_keys"
    key = Column(String, primary_key=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

class Address(Base):
    __tablename__ = "addresses"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    great_city = Column(String)
    state = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    lat = Column(Float)
    lon = Column(Float)

    restaurant_id = Column(String, ForeignKey('restaurant.id'), unique=True)
    restaurant = relationship("Restaurant", back_populates="address")

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
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    open_now = Column(Enum(search_enums.OpenNowEnum), nullable=False)
    

    # Link to Address model
    #address_id = Column(String, ForeignKey('addresses.id'))


    opening_hours = relationship("OpeningHours", back_populates="restaurant")
    # One-to-one relationship with Address
    address = relationship("Address", back_populates="restaurant", uselist=False)
    # One-to-many relationship with Dishes
    dishes = relationship("Dish", back_populates="restaurant")


class OpeningHours(Base):
    __tablename__ = 'opening_hours'

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    day_of_week = Column(Enum(search_enums.DayOfWeekEnum), nullable=False)
    open_time = Column(Time, nullable=False, default="09:00")
    close_time = Column(Time, nullable=False, default="17:00")
    restaurant_id = Column(String, ForeignKey('restaurant.id'))

    restaurant = relationship("Restaurant", back_populates="opening_hours")

class Dish(Base):
    __tablename__ = "dishes"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    menu_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    diet = Column(Enum(search_enums.DietEnum), nullable=False)
    food_type = Column(Enum(search_enums.FoodTypeEnum), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    podcast_name = Column(String, nullable=False)

    restaurant_id = Column(String, ForeignKey("restaurant.id"))
    restaurant = relationship("Restaurant", back_populates="dishes")
    
    # One-to-many relationship with OtherItems
    other_items = relationship("OtherItem", back_populates="dish")
    content = relationship("Content", back_populates="dish", uselist=False)


class Content(Base):
    __tablename__ = "content_dish"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    video_file_path = Column(String, nullable=True)  
    card_photo_file_path = Column(String, nullable=True) 
    podcast_file_path = Column(String, nullable=True)  
    filler_photos = Column(JSON, nullable=True) 

    dish_id = Column(String(length=36), ForeignKey('dishes.id'))
    dish = relationship("Dish", back_populates="content")


class OtherItem(Base):
    __tablename__ = "other_items"

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    dish_id = Column(String, ForeignKey("dishes.id"))

    dish = relationship("Dish", back_populates="other_items")

