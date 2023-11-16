from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator
from datetime import datetime, time, timezone
from app.enums import search_enums
from app.schema.DishSchema import Dish


#from app.schema.DishSchema import Dish

#Create Restaurant base model

from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime, time, timezone

class CheckOpenNow(BaseModel):
    day_of_week: search_enums.DayOfWeekEnum
    current_time: str

    @validator("current_time", pre=True)
    def validate_time_format(cls, value: str) -> str:
        time_format = "%H:%M"
        try:
            datetime.strptime(value, time_format)
            return value
        except ValueError:
            raise ValueError(f"Time {value} is not in the correct format {time_format}")

class OpeningHoursBase(BaseModel):
    day_of_week: search_enums.DayOfWeekEnum
    open_time: time = time(9, 0)
    close_time: time = time(17, 0)

class OpenRestaurantResponse(BaseModel):
    open_restaurants: List[str]

class OpeningHoursCreate(OpeningHoursBase):
    pass

class OpeningHoursListCreate(BaseModel):
    hours: List[OpeningHoursCreate]

class OpeningHours(OpeningHoursBase):
    id: Optional[str]
    restaurant_id: Optional[str]


# Address Model
class AddressBase(BaseModel):
    street: str
    city: str
    great_city: str
    state: str
    zipcode: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: Optional[str]
    restaurant_id: Optional[str]
    lat: Optional[float]
    lon: Optional[float]


class RestaurantLocationUpdate(BaseModel):
    name: str
    lat: float
    lon: float

# Restaurant Models
class RestaurantBase(BaseModel):
    name: str
    chef_name: str
    cuisine: search_enums.CuisineEnum
    establishment_type: search_enums.EstablishmentTypeEnum
    address: AddressBase
    description: str
    menu: str
    instagram: str
    is_active: bool
    open_now: search_enums.OpenNowEnum

    @validator("name")
    def validate_name(cls, name: str):
        if len(name) < 3:
            raise ValueError("Restaurant name should be at least 3 characters long.")
        return name

class RestaurantUpdate(BaseModel):
    chef_name: str
    cuisine: search_enums.CuisineEnum
    establishment_type: search_enums.EstablishmentTypeEnum
    address: AddressBase
    description: str
    menu: str
    instagram: str
    is_active: bool
    open_now: search_enums.OpenNowEnum


class RestaurantCreate(RestaurantBase):
    pass

class DeleteRestaurant(BaseModel):
    message: str

class Restaurant(RestaurantBase):
    id: Optional[str]
    date_created: Optional[datetime]
    opening_hours: Optional[List[OpeningHoursBase]] = []
    dishes: Optional[List[Dish]] = []

