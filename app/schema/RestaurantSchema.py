from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator
from datetime import datetime, time
from app.enums import search_enums
from app.schema.DishSchema import Dish

#from app.schema.DishSchema import Dish

#Create Restaurant base model

class OpeningHoursBase(BaseModel):
    day_of_week: search_enums.DayOfWeekEnum
    open_time: time
    close_time: time

class OpeningHoursCreate(OpeningHoursBase):
    pass

class OpeningHours(OpeningHoursBase):
    id: Optional[str]
    restaurant_id: Optional[str]

    class Config:
        orm_mode = True

# Restaurant Models

class RestaurantBase(BaseModel):
    name: str
    chef_name: str
    cuisine: search_enums.CuisineEnum
    establishment_type: search_enums.EstablishmentTypeEnum
    address: str
    description: str
    menu: str
    instagram: str
    is_active: bool
    open_now: search_enums.OpenNowEnum
    lat: Optional[str]
    lon: Optional[str]

    # Adding a basic validator as an example
    @validator("name")
    def validate_name(cls, name):
        if len(name) < 3:
            raise ValueError("Restaurant name should be at least 3 characters long.")
        return name

class RestaurantCreate(RestaurantBase):
    pass

class DeleteRestaurant(BaseModel):
    message: str


class Restaurant(RestaurantBase):
    id: Optional[str]
    date_created: Optional[datetime]
    opening_hours: Optional[List[OpeningHoursBase]] = []
    dishes: Optional[List[Dish]] = []

    class Config:
        orm_mode = True



