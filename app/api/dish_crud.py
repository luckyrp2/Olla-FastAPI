from sqlalchemy.orm import Session
from app.models import models
from app.schema import DishSchema
from app.models import models
from app.enums import search_enums
from sqlalchemy import and_
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import time
from typing import List, Optional

from app.models import models

# CRUD for Dish
def create_dish_for_restaurant(db: Session, restaurant_name: str, dish_data: DishSchema.DishCreate):
    # Fetch the restaurant by its name
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_name).first()
    
    # Raise an error if no restaurant is found
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Create the Dish instance with the restaurant's ID
    db_dish = models.Dish(**dish_data.dict(), restaurant_id=restaurant.id)
    
    # Add to the session and commit
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    
    return db_dish



def get_dishes_by_food_type(db: Session, food_type: search_enums.FoodTypeEnum) -> List[DishSchema.DishWithRestaurant]:
    dishes = (
        db.query(models.Dish)
        .options(joinedload(models.Dish.restaurant))  # Ensure that the Restaurant data is loaded along with the Dish
        .filter(models.Dish.food_type == food_type)
        .all()
    )
    
    results = []
    for dish in dishes:
        dish_data = {
            "id": dish.id,
            "date_added": dish.date_added,
            "menu_name": dish.menu_name,
            "stars": dish.stars,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "description": dish.description,
            "is_active": dish.is_active,
            "restaurant_info": {
                "restaurant_id": dish.restaurant.id,
                "restaurant_name": dish.restaurant.name
            },
            "other_items": [{"id": item.id, "name": item.name, "image_link": item.image_link} for item in dish.other_items],
            # Adding default values for the new fields
            "podcast_name": dish.podcast_name,
            "podcast_file_path": dish.podcast_file_path,
            "video_file_path": dish.video_file_path,
            "card_photo_file_path": dish.card_photo_file_path,
            "filler_photos": dish.filler_photos
        }
        
        results.append(DishSchema.DishWithRestaurant(**dish_data))
    
    return results

def get_dishes_by_diet(db: Session, diet_type: search_enums.DietEnum) -> List[DishSchema.DishWithRestaurant]:
    dishes = (
        db.query(models.Dish)
        .options(joinedload(models.Dish.restaurant))  # Ensure that the Restaurant data is loaded along with the Dish
        .filter(models.Dish.diet == diet_type)
        .all()
    )
    
    results = []
    for dish in dishes:
        dish_data = {
            "id": dish.id,
            "date_added": dish.date_added,
            "menu_name": dish.menu_name,
            "stars": dish.stars,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "description": dish.description,
            "is_active": dish.is_active,
            "restaurant_info": {
                "restaurant_id": dish.restaurant.id,
                "restaurant_name": dish.restaurant.name
            },
            "other_items": [{"id": item.id, "name": item.name, "image_link": item.image_link} for item in dish.other_items],
            # Adding default values for the new fields
            "podcast_name": dish.podcast_name,
            "podcast_file_path": dish.podcast_file_path,
            "video_file_path": dish.video_file_path,
            "card_photo_file_path": dish.card_photo_file_path,
            "filler_photos": dish.filler_photos
        }
        
        results.append(DishSchema.DishWithRestaurant(**dish_data))
    
    return results

def get_all_dishes(db: Session) -> List[models.Dish]:
    """Retrieve all dishes in the database."""
    return db.query(models.Dish).all()

def get_dishes(db: Session, 
               diet_type: Optional[search_enums.DietEnum] = None, 
               cuisine: Optional[search_enums.CuisineEnum] = None,
               establishment: Optional[search_enums.EstablishmentTypeEnum]= None) -> List[DishSchema.DishWithRestaurant]:
    
    # Base query
    query = db.query(models.Dish).options(joinedload(models.Dish.restaurant))
    
    # Apply filter based on diet type if provided
    if diet_type:
        query = query.filter(models.Dish.diet == diet_type)
    
    # Apply filter based on cuisine if provided
    if cuisine:
        query = query.join(models.Restaurant, models.Dish.restaurant_id == models.Restaurant.id)\
                     .filter(models.Restaurant.cuisine == cuisine)

    dishes = query.all()
    
    results = []
    for dish in dishes:
        dish_data = {
            "id": dish.id,
            "date_added": dish.date_added,
            "menu_name": dish.menu_name,
            "stars": dish.stars,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "description": dish.description,
            "is_active": dish.is_active,
            "restaurant_info": {
                "restaurant_id": dish.restaurant.id,
                "restaurant_name": dish.restaurant.name
            },
            "other_items": [{"id": item.id, "name": item.name, "image_link": item.image_link} for item in dish.other_items],
            # Adding default values for the new fields
            "podcast_name": dish.podcast_name,
            "podcast_file_path": dish.podcast_file_path,
            "video_file_path": dish.video_file_path,
            "card_photo_file_path": dish.card_photo_file_path,
            "filler_photos": dish.filler_photos
        }
        results.append(DishSchema.DishWithRestaurant(**dish_data))
    
    return results

def get_dishes_from_open_restaurants(db: Session, current_time: time, current_day: int):
    open_restaurants = db.query(models.Restaurant).join(
        models.OpeningHours,
        and_(
            models.Restaurant.id == models.OpeningHours.restaurant_id,
            models.OpeningHours.day_of_week == current_day,
            models.OpeningHours.open_time <= current_time,
            models.OpeningHours.close_time >= current_time
        )
    ).all()

    dishes = []
    for restaurant in open_restaurants:
        for dish in restaurant.dishes:
            dishes.append(dish)

    return dishes
