from typing import List, Optional
from pydantic import BaseModel, validator
from app.enums import search_enums  # Replace with your actual import path
from datetime import datetime, time
# ... [other schema classes]

# Define your Dish schemas

class OtherItemBase(BaseModel):
    name: str
    image_link: str

class OtherItemCreate(OtherItemBase):
    pass

class OtherItem(OtherItemBase):
    id: Optional[str]
    dish_id: Optional[str]

    class Config:
        orm_mode = True

class DishBase(BaseModel):
    date_added: datetime
    menu_name: str
    stars: int
    diet: search_enums.DietEnum
    food_type: search_enums.FoodTypeEnum
    description: str
    is_active: bool

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: Optional[str]
    restaurant_id: Optional[str]
    items: Optional[List[OtherItem]] = []

    class Config:
        orm_mode = True