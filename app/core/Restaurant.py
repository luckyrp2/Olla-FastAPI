from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema import RestaurantSchema
from app.api import restaurant_crud
from app.database import configuration
from app.enums import search_enums
from app.func import geo_location
from typing import List

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")


# Function to get a database session
get_db = configuration.get_db

@router.post("/new",
             response_model=RestaurantSchema.Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
def create_new_restaurant(restaurant: RestaurantSchema.RestaurantCreate, db: Session = Depends(get_db)):
    # Commented out code removed for clarity
    return restaurant_crud.create_restaurant(db=db, restaurant=restaurant)

@router.delete("/delete/{restaurant_name}",
               response_model=RestaurantSchema.DeleteRestaurant,
               summary="Delete a Restaurant by its name")
def delete_restaurant_by_name(restaurant_name: str, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_by_name(db, restaurant_name)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_crud.delete_restaurant(db, db_restaurant.id)
    return {"message": f"Restaurant {restaurant_name} deleted successfully!"}

@router.get("/cuisine/{cuisine}", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Find Restaurant by Cuisine", 
            status_code=status.HTTP_200_OK)
def get_restaurant_cuisine(cuisine: search_enums.CuisineEnum, db: Session = Depends(get_db)):
    db_restaurants = restaurant_crud.get_restaurant_by_cuisine(db, cuisine=cuisine)
    
    # If the list of restaurants is empty, raise an exception
    if not db_restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurants


@router.get("/restaurant/{restaurant_name}", 
            response_model=RestaurantSchema.Restaurant, 
            summary="Find Restaurant by Name", 
            status_code=status.HTTP_200_OK)
def get_restaurant_by_name_endpoint(restaurant_name: str, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_by_name(db, restaurant_name=restaurant_name)
    
    # If no restaurant is found, raise an exception
    if not db_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurant


@router.get("/establishment/{establishment_type}", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Find Restaurant by Establishment Type", 
            status_code=status.HTTP_200_OK)
def get_restaurant_establishment(establishment_type: search_enums.EstablishmentTypeEnum, db: Session = Depends(get_db)):
    db_restaurants = restaurant_crud.get_restaurant_by_establishment_type(db, establishment_type=establishment_type)
    
    # If the list of restaurants is empty, raise an exception
    if not db_restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurants


@router.post("/hours/{name}", 
             response_model=RestaurantSchema.Restaurant, 
             summary="Add Opening Hours", 
             status_code=status.HTTP_200_OK)
def get_opening_hours(opening_hours_create: RestaurantSchema.OpeningHoursCreate, name: str, db: Session = Depends(get_db)):
    db_restaurant = restaurant_crud.get_restaurant_id_by_name(db=db, name=name)
    
    # Add opening hours and return the updated restaurant object
    return restaurant_crud.add_opening_hours(db=db, restaurant_id=db_restaurant.id, opening_hours_create=opening_hours_create)
