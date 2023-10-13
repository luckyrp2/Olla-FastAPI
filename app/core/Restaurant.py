from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema.RestaurantSchema import Restaurant
from app.api import restaurant_crud
from app.database import configuration

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")

#creating a database
get_db = configuration.get_db

#response_model controls input
@router.post("/new",
             response_model=Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
#pydantic verificiation first entry
def r_restaurant(restaurant: Restaurant, db: Session = Depends(get_db)):
    #check if restaurant exists
    db_restaurant = restaurant_crud.get_restaurant_by_id(db,
                                             id = restaurant.id,
                                             date = restaurant.date_added,
                                             name = restaurant.name,
                                             chef_name = restaurant.chef_name)
    if db_restaurant:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Restaurant already exists")
    return restaurant_crud.create_restaurant(db=db, restaurant=restaurant)

