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

@router.get("/food_type/{food_type}", response_model=List[DishSchema.DishWithRestaurant], summary="Find all Dishes with Food Type",
             status_code=status.HTTP_200_OK)
def get_dishes_by_type(food_type: search_enums.FoodTypeEnum, db: Session = Depends(get_db)):
    return dish_crud.get_dishes_by_food_type(db, food_type)

@router.get("/diet/{diet_type}", response_model=List[DishSchema.DishWithRestaurant], summary="Find all Dishes by Diet Type", status_code=status.HTTP_200_OK)
def get_dishes_by_diet(diet_type: search_enums.DietEnum, db: Session = Depends(get_db)):
    return dish_crud.get_dishes(db, diet_type=diet_type)

@router.get("/cuisine/{cuisine}", response_model=List[DishSchema.DishWithRestaurant], summary="Find all Dishes by Cuisine", status_code=status.HTTP_200_OK)
def get_dishes_by_cuisine(cuisine: search_enums.CuisineEnum, db: Session = Depends(get_db)):
    return dish_crud.get_dishes(db, cuisine=cuisine)

@router.get("/establishment/{establishment}", response_model=List[DishSchema.DishWithRestaurant], summary="Find all Dishes by Cuisine", status_code=status.HTTP_200_OK)
def get_dishes_by_cuisine(establishment: search_enums.EstablishmentTypeEnum, db: Session = Depends(get_db)):
    return dish_crud.get_dishes(db, establishment=establishment)

@router.get("/all", 
            response_model=List[DishSchema.Dish], 
            summary="Get All Dishes", 
            status_code=status.HTTP_200_OK)
def get_all_dishes_endpoint(db: Session = Depends(get_db)):
    return dish_crud.get_all_dishes(db)