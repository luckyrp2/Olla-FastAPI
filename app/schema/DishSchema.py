'''
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import UUID4, BaseModel
from pydantic.networks import EmailStr
from datetime import datetime

from app.schema.DishSchema import Content

#Create Restaurant base model
class DishBase(BaseModel):
    date_added: datetime
    menu_name: str
    stars: int
    description: str
    other_items: str
    is_active: bool

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: UUID4
    restaurant_id: int
    content: Content

    class Config: 
        orm_mode = True


'''