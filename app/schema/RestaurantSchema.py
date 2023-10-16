from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import UUID4, BaseModel
from pydantic.networks import EmailStr
from datetime import datetime

#Create Restaurant base model
class RestaurantBase(BaseModel):
    id: int
    date_added: datetime
    name: str
    chef_name: str
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


