from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema import RestaurantSchema
from app.api import restaurant_crud
from app.database import configuration

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")

#creating a database
get_db = configuration.get_db

#response_model controls input
@router.post("/new",
             response_model=RestaurantSchema.Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
def create_new_restaurant(restaurant: RestaurantSchema.RestaurantBase, db: Session = Depends(get_db)):
    #db_restaurant = restaurant_crud.get_restaurant_by_id(db,
                                             #id = restaurant.id)
   # if db_restaurant:
   #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                        detail="Restaurant already exists")
    return restaurant_crud.create_restaurant(db=db, restaurant=restaurant)
'''
@router.get("/id", response_model=RestaurantBase, summary="Find Restaurant by ID", status_code=status.HTTP_200_OK)
def get_restaurant_id(id: int, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_by_id(db, id = id)
    if db_restaurant is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return db_restaurant
'''

