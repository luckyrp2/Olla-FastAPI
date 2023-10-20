from sqlalchemy.orm import Session
from app.models import models
from app.schema import DishSchema
from app.models import models
from app.enums import search_enums

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import time

from app.models import models

# CRUD for Dish

def create_dish_for_restaurant(db: Session, restaurant_name: str, dish: DishSchema.DishCreate):
    # First, fetch the restaurant by its name
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_name).first()
    
    # If no restaurant is found with the provided name, raise an error
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Create the Dish instance and associate it with the fetched restaurant
    db_dish = models.Dish(**dish.dict(), restaurant_id=restaurant.id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    
    return db_dish