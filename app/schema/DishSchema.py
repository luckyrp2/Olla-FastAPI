from typing import List, Optional
from pydantic import BaseModel, validator
from app.enums import search_enums  # Replace with your actual import path
from datetime import datetime, time
# ... [other schema classes]

# ... [Your existing Pydantic models]

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.enums import search_enums

# Other Item Models
class OtherItemBase(BaseModel):
    name: str
    image_link: str

class OtherItemCreate(OtherItemBase):
    pass

class OtherItem(OtherItemBase):
    id: Optional[str]
    dish_id: Optional[str]


# Content Information Model
class ContentInfo(BaseModel):
    podcast_file_path: Optional[str] = None
    video_file_path: Optional[str] = None
    card_photo_file_path: Optional[str] = None
    filler_photos: Optional[List[str]] = []

# Dish Models
class DishBase(BaseModel):
    date_added: datetime
    menu_name: str
    stars: int
    diet: search_enums.DietEnum
    food_type: search_enums.FoodTypeEnum
    description: str
    is_active: bool
    podcast_name: Optional[str]

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: Optional[str]
    restaurant_id: Optional[str]
    other_items: Optional[List[OtherItem]] = []
    content: Optional[ContentInfo] = []

# Restaurant Information Model
class RestaurantInfo(BaseModel):
    restaurant_id: str
    restaurant_name: str

# Dish with Restaurant Information
class DishWithRestaurant(DishBase):
    restaurant_info: RestaurantInfo


