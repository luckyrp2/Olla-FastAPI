from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema.RestaurantSchema import Restaurant
from app.api import restaurant_crud
from app.database import configuration

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")
get_db = configuration.get_db

@router.post("/new",
             response_model=Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
def r_restaurant(restaurant: Restaurant, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.create_restaurant(db,
                                             id = restaurant.id,
                                             date = restaurant.date_added,
                                             name = restaurant.name,
                                             chef_name = restaurant.chef_name)
    if db_restaurant:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")
    return restaurant_crud.create_pilot_user(db=db, restaurant=restaurant)

