from sqlalchemy.orm import Session
from app.schema import DishSchema
from app.models import models
from app.enums import search_enums
from sqlalchemy import and_
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import time
from typing import List, Optional
from app.func.s3_amazon import get_content, FileType
import random
from app.models import models

# CRUD for Dish
def create_dish_for_restaurant(db: Session, restaurant_name: str, dish: DishSchema.DishCreate):
    # Fetch the restaurant by its name
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_name).first()
    
    # Raise an error if no restaurant is found
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Create the Dish instance with the restaurant's ID
    db_dish = models.Dish(**dish.dict(), restaurant_id=restaurant.id)
    
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
            "calories": dish.calories,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "course_type": dish.course_type,
            "description": dish.description,
            "is_active": dish.is_active,
            "restaurant_info": {
                "restaurant_id": dish.restaurant.id,
                "restaurant_name": dish.restaurant.name
            },
            "other_items": [{"id": item.id, "name": item.name, "image_link": item.image_link} for item in dish.other_items],
            # Adding default values for the new fields
            "podcast_name": dish.podcast_name,
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
            "calories": dish.calories,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "course_type": dish.course_type,
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
            "calories": dish.calories,
            "diet": dish.diet,
            "food_type": dish.food_type,
            "course_type": dish.course_type,
            "description": dish.description,
            "is_active": dish.is_active,
            "restaurant_info": {
                "restaurant_id": dish.restaurant.id,
                "restaurant_name": dish.restaurant.name
            },
            "other_items": [{"id": item.id, "name": item.name, "image_link": item.image_link} for item in dish.other_items],
            # Adding default values for the new fields
            "podcast_name": dish.podcast_name,
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


def update_dish_content_paths(db: Session) -> List[models.Dish]:
    # Fetch all dishes, along with their related content
    dishes = db.query(models.Dish).options(joinedload(models.Dish.content)).all()


    updated_dishes = []
    for dish in dishes:

        # Check if dish.content exists, if not, create a new Content object
        if not dish.content:
            dish.content = models.Content(dish_id=dish.id)

        # Update podcast file path
        podcast_urls = get_content(dish.restaurant.name, dish.menu_name, FileType.podcast_file_path)
        if podcast_urls:
            dish.content.podcast_file_path = podcast_urls[0]

        # Update video file path
        video_urls = get_content(dish.restaurant.name, dish.menu_name, FileType.video_file_path)
        if video_urls:
            dish.content.video_file_path = video_urls[0]

        # Update card photo file path
        cover_image_urls = get_content(dish.restaurant.name, dish.menu_name, FileType.card_photo_file_path)
        print(cover_image_urls)
        if cover_image_urls:
            dish.content.card_photo_file_path = cover_image_urls[0]
        
        additional_images_urls = get_content(dish.restaurant.name, dish.menu_name, FileType.filler_photos)
        if additional_images_urls:
            dish.content.filler_photos = additional_images_urls

        db.commit()
        db.refresh(dish)
        updated_dishes.append(dish)

    return updated_dishes

def get_or_update_featured_dish(db: Session, update: bool):
    if update:
        # Reset the is_featured flag for all dishes
        db.query(models.Dish).update({models.Dish.is_featured: False})

        # Randomly select a new dish to feature
        dishes = db.query(models.Dish).all()
        if not dishes:
            return None
        featured_dish = random.choice(dishes)
        featured_dish.is_featured = True
    else:
        # Fetch the currently featured dish
        featured_dish = db.query(models.Dish).filter(models.Dish.is_featured == True).first()
        if not featured_dish:
            # Handle the case where no dish is currently featured
            return None

    db.commit()
    return featured_dish
