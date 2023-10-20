from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema import RestaurantSchema, DishSchema
from app.api import restaurant_crud, dish_crud
from app.database import configuration
from app.enums import search_enums
from app.func import geo_location
from typing import List

router = APIRouter(tags=["Dish"], prefix="/dish")

# Function to get a database session
get_db = configuration.get_db

@router.post("/new/{restaurant_name}", response_model=DishSchema.DishBase, summary="Add Dish Based on Restaurant Name",
             status_code=status.HTTP_201_CREATED)
def create_dish_for_restaurant(restaurant_name: str, dish: DishSchema.DishCreate, db: Session = Depends(get_db)):
    return dish_crud.create_dish_for_restaurant(db=db, restaurant_name=restaurant_name, dish=dish)