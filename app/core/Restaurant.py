from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema import RestaurantSchema
from app.api import restaurant_crud
from app.database import configuration
from app.enums import search_enums
from app.func import geo_location
from typing import List
from app.database.api_security import get_api_key

router = APIRouter(tags=["Restaurant"], prefix="/restaurant")


# Function to get a database session
get_db = configuration.get_db

router = APIRouter()

@router.post("/new",
             response_model=RestaurantSchema.Restaurant,
             summary="Make a new Restaurant",
             status_code=status.HTTP_201_CREATED)
def create_new_restaurant(
    restaurant: RestaurantSchema.RestaurantCreate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)):
    
    return restaurant_crud.create_restaurant(db=db, restaurant=restaurant)


@router.delete("/delete/{restaurant_name}",
               response_model=RestaurantSchema.DeleteRestaurant,
               summary="Delete a Restaurant by its name")
def delete_restaurant_by_name(restaurant_name: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_restaurant = restaurant_crud.get_restaurant_by_name(db, restaurant_name)
    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant_crud.delete_restaurant(db, db_restaurant.id)
    return {"message": f"Restaurant {restaurant_name} deleted successfully!"}

@router.get("/cuisine/{cuisine}", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Find Restaurant by Cuisine", 
            status_code=status.HTTP_200_OK)
def get_restaurant_cuisine(cuisine: search_enums.CuisineEnum, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_restaurants = restaurant_crud.get_restaurant_by_cuisine(db, cuisine=cuisine)
    
    # If the list of restaurants is empty, raise an exception
    if not db_restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurants


@router.get("/restaurant_name/{restaurant_name}", 
            response_model=RestaurantSchema.Restaurant, 
            summary="Find Restaurant by Name", 
            status_code=status.HTTP_200_OK)
def get_restaurant_by_name_endpoint(restaurant_name: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_restaurant = restaurant_crud.get_restaurant_by_name(db, restaurant_name=restaurant_name)
    
    # If no restaurant is found, raise an exception
    if not db_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurant


@router.get("/establishment/{establishment_type}", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Find Restaurant by Establishment Type", 
            status_code=status.HTTP_200_OK)
def get_restaurant_establishment(establishment_type: search_enums.EstablishmentTypeEnum, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_restaurants = restaurant_crud.get_restaurant_by_establishment_type(db, establishment_type=establishment_type)
    
    # If the list of restaurants is empty, raise an exception
    if not db_restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    
    return db_restaurants


@router.post("/hours/{name}", 
             response_model=RestaurantSchema.Restaurant, 
             summary="Add Opening Hours", 
             status_code=status.HTTP_200_OK)
def get_opening_hours(opening_hours_create: RestaurantSchema.OpeningHoursCreate, name: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_restaurant = restaurant_crud.get_restaurant_id_by_name(db=db, name=name)
    
    # Add opening hours and return the updated restaurant object
    return restaurant_crud.add_opening_hours(db=db, restaurant_id=db_restaurant.id, opening_hours_create=opening_hours_create)

@router.get("/all", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Get All Restaurants", 
            status_code=status.HTTP_200_OK)
def get_all_restaurants_endpoint(db: Session = Depends(get_db)):
    return restaurant_crud.get_all_restaurants(db)

@router.get("/restaurant_id/{restaurant_id}", response_model=RestaurantSchema.RestaurantBase, summary="Get Restaurant by ID", status_code=status.HTTP_200_OK)
def get_restaurant(restaurant_id: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    restaurant = restaurant_crud.get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.get("/restaurants_by_city/{greater_city}", 
            response_model=List[RestaurantSchema.Restaurant], 
            summary="Get All Restaurants by Greater City Area", 
            status_code=status.HTTP_200_OK)
def get_restaurants_by_city(greater_city: str, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    restaurants = restaurant_crud.get_restaurants_by_greater_city(db, greater_city)
    if not restaurants:
        raise HTTPException(status_code=404, detail=f"No restaurants found in {greater_city} area.")
    return restaurants

@router.put("/update_lat_lon",
            response_model=List[RestaurantSchema.RestaurantLocationUpdate],
            summary="Update Missing Lat and Lon for Restaurants",
            status_code=status.HTTP_200_OK)
def update_lat_lon_for_restaurants(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    # Use the previously defined function to update the restaurants with missing lat/lon
    return restaurant_crud.update_missing_lat_lon(db)
    
@router.put("/check-open-now", 
            response_model=RestaurantSchema.OpenRestaurantResponse, 
            summary="Check and Update Restaurants Open Now", 
            status_code=status.HTTP_200_OK)
def check_and_update_open_now(check_data: RestaurantSchema.CheckOpenNow, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    open_restaurants = restaurant_crud.get_open_restaurants(db=db, day_of_week=check_data.day_of_week.value, current_time_str=check_data.current_time)
    return {"open_restaurants": open_restaurants}

@router.put("/update/{restaurant_name}", response_model=RestaurantSchema.Restaurant)  # Update with your correct schema
def update_restaurant(restaurant_name: str, update_data: RestaurantSchema.RestaurantUpdate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    updated_restaurant = restaurant_crud.update_restaurant_by_name(db, restaurant_name, update_data.dict())
    if not updated_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated_restaurant

@router.delete("/delete_inactive_restaurants", status_code=status.HTTP_200_OK)
def delete_inactive_restaurants_endpoint(db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    count = restaurant_crud.delete_inactive_restaurants(db)
    if count > 0:
        return {"message": f"Deleted {count} inactive restaurants and their associated dishes"}
    else:
        return {"message": "No inactive restaurants found to delete"}