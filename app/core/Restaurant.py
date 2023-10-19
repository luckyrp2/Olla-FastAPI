from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema import RestaurantSchema
from app.api import restaurant_crud
from app.database import configuration
from app.enums import search_enums
from app.func import geo_location
router = APIRouter(tags=["Restaurant"], prefix="/restaurant")

#creating a database
get_db = configuration.get_db

#response_model controls input
@router.post("/new",
             response_model=RestaurantSchema.Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
def create_new_restaurant(restaurant: RestaurantSchema.RestaurantCreate, db: Session = Depends(get_db)):
    #db_restaurant = restaurant_crud.get_restaurant_by_id(db,
                                             #id = restaurant.id)
   # if db_restaurant:
   #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                        detail="Restaurant already exists")
    return restaurant_crud.create_restaurant(db=db, restaurant=restaurant)

@router.get("/{cuisine}", response_model=RestaurantSchema.Restaurant, summary="Find Restaurant by Cuisine", status_code=status.HTTP_200_OK)
def get_restaurant_cuisine(cuisine: search_enums.CuisineEnum, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_by_cuisine(db, cuisine = cuisine)
    if db_restaurant is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return db_restaurant

@router.get("/{establishment_type}", response_model=RestaurantSchema.Restaurant, summary="Find Restaurant by Establishment Type", status_code=status.HTTP_200_OK)

def get_restaurant_establishment(establishment_type: str, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_by_establishment_type(db, establishemnt_type= establishment_type)
    if db_restaurant is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return db_restaurant

@router.post("/hours/{name}", response_model=RestaurantSchema.Restaurant, summary="Add Opening Hours", status_code=status.HTTP_200_OK)

def get_opening_hours(opening_hours_create: RestaurantSchema.OpeningHoursCreate, name: str, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_id_by_name(db=db, name=name)
    return restaurant_crud.add_opening_hours(db=db, restaurant_id=db_restaurant.id, opening_hours_create=opening_hours_create)