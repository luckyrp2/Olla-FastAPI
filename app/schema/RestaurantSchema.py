from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel
from app.models.models import OpeningHours
from pydantic.networks import EmailStr
from datetime import datetime, time
from app.enums import search_enums

#from app.schema.DishSchema import Dish

#Create Restaurant base model

class OpeningHoursBase(BaseModel):
    day_of_week: search_enums.DayOfWeekEnum
    open_time: time
    close_time: time

class OpeningHoursCreate(OpeningHoursBase):
    pass


class OpeningHours(OpeningHoursBase):
    id: str
    restaurant_id: str

    class Config:
        orm_mode = True

class RestaurantBase(BaseModel):
    name: str 
    chef_name: str 
    cuisine: search_enums.CuisineEnum
    establishment_type: search_enums.EstablishmentTypeEnum
    address: str
    description: str 
    is_active: bool
    open_now: search_enums.OpenNowEnum

class RestaurantCreate(RestaurantBase): 
    pass

class RestaurantResponse(RestaurantBase):
    opening_hours: List[OpeningHours] = []

class Restaurant(RestaurantBase):
    id: str
    date_created: datetime
    opening_hours: List[OpeningHours] = []

    #featured: List[Dish] = []

    #lass Config:
     #   from_attributes = True




