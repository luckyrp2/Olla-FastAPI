from typing import List, Optional
from pydantic import BaseModel, validator
from app.enums import search_enums  # Replace with your actual import path
from datetime import datetime, time
# ... [other schema classes]

# ... [Your existing Pydantic models]

class OtherItemBase(BaseModel):
    name: str
    image_link: str

class OtherItemCreate(OtherItemBase):
    pass

class OtherItem(OtherItemBase):
    id: Optional[str]
    dish_id: Optional[str]

    class Config:
        from_orm = True

class DishBase(BaseModel):
    date_added: datetime
    menu_name: str
    stars: int
    diet: search_enums.DietEnum
    food_type: search_enums.FoodTypeEnum
    description: str
    is_active: bool

    podcast_name: Optional[str]
    podcast_file_path: Optional[str]
    video_file_path: Optional[str]
    card_photo_file_path: Optional[str]
    filler_photos: Optional[List[str]]

class DishCreate(DishBase):
    pass
    

class RestaurantInfo(BaseModel):
    restaurant_id: str
    restaurant_name: str

class DishWithRestaurant(DishBase):
    restaurant_info: RestaurantInfo

class Dish(DishBase):
    id: Optional[str]
    restaurant_id: Optional[str]
    other_items: Optional[List[OtherItem]] = []

    class Config:
        from_orm = True
