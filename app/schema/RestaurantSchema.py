from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel
from pydantic.networks import EmailStr


class RestaurantBase(BaseModel):
    id: Optional[str]
    name: Optional[str]
    chef_name: Optional[str]
    food_category: Optional[str]
    menu_name: Optional[str]
    stars: Optional[int]
    location: Optional[str]
    address: Optional[str]
    podcast_file_path: Optional[str]
    video_file_path: Optional[str]
    card_photo_file_path: Optional[str]
    menu_list_photo_file_path: Optional[str]
    podcast_name: Optional[str]
    description: Optional[str]
    other_item_name: Optional[str]
    flags: Optional[str]

