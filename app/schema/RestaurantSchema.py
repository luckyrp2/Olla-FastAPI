from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import UUID4, BaseModel
from pydantic.networks import EmailStr
from datetime import datetime

#from app.schema.DishSchema import Dish

#Create Restaurant base model
class RestaurantBase(BaseModel):
    name: str 
    chef_name: str 
    address: str 
    description: str 
    is_active: bool

class RestaurantCreate(RestaurantBase): 
    pass

class Restaurant(RestaurantBase):
    id: UUID4
    #featured: List[Dish] = []

    #class Config:
    #    orm_mode = True



    '''
    food_category: Optional[str]
    menu_name: Optional[str]
    stars: Optional[int]
    location: Optional[str]
    address: Optional[str]
    video_file_path: Optional[str]
    card_photo_file_path: Optional[str]
    menu_list_photo_file_path: Optional[str]
    podcast_name: Optional[str]
    description: Optional[str]
    other_item_name: Optional[str]
    podcast_file_path: Optional[str]
    '''


