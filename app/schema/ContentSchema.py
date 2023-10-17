'''
from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import UUID4, BaseModel
from pydantic.networks import EmailStr
from datetime import datetime

#Create Restaurant base model
class ContentBase(BaseModel):
    podcast_name: str

class Content(ContentBase):
    id: int
    restaurant_id: int



    class Config: 
        orm_mode = True

'''