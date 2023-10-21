from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import time

from app.models import models
from app.schema import RestaurantSchema
from app.enums import search_enums
from app.func import geo_location
from typing import List

def create_restaurant(db: Session, restaurant: RestaurantSchema.RestaurantCreate) -> models.Restaurant:
    """
    Create a new restaurant in the database.

    Args:
    - db: Database session.
    - restaurant (RestaurantSchema.RestaurantCreate): Restaurant data to insert.

    Returns:
    - models.Restaurant: The created restaurant.
    """
    new_restaurant = models.Restaurant(
        name=restaurant.name,
        chef_name=restaurant.chef_name,
        cuisine=restaurant.cuisine,
        instagram=restaurant.instagram,
        menu=restaurant.menu,
        establishment_type=restaurant.establishment_type,
        address=restaurant.address,
        description=restaurant.description,
        is_active=restaurant.is_active,
        open_now=restaurant.open_now
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

def get_restaurant_by_cuisine(db: Session, cuisine: str) -> list:
    """Retrieve restaurants by cuisine type."""
    restaurants = db.query(models.Restaurant).filter(cuisine == models.Restaurant.cuisine).all()
    if not restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurants with given cuisine not found")
    return restaurants

def get_restaurant_by_establishment_type(db: Session, establishment_type: str) -> list:
    """Retrieve restaurants by establishment type."""
    restaurants = db.query(models.Restaurant).filter(establishment_type == models.Restaurant.establishment_type).all()
    if not restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurants with given establishment type not found")
    return restaurants

def get_restaurant_id_by_name(db: Session, name: str) -> models.Restaurant:
    """Retrieve restaurant by name."""
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == name).first()
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with name {name} not found")
    return restaurant

def add_opening_hours(db: Session, restaurant_id: str, opening_hours_create: RestaurantSchema.OpeningHoursCreate) -> models.Restaurant:
    """
    Add or update opening hours for a restaurant.
    Hours must be in format 08:00 for anything below 10.

    Args:
    - db: Database session.
    - restaurant_id (str): ID of the restaurant to update.
    - opening_hours_create (RestaurantSchema.OpeningHoursCreate): New opening hours data.

    Returns:
    - models.Restaurant: The updated restaurant with the associated opening hours.
    """
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with id {restaurant_id} not found")

    existing_hours = db.query(models.OpeningHours).filter(
        models.OpeningHours.restaurant_id == restaurant_id,
        models.OpeningHours.day_of_week == opening_hours_create.day_of_week
    ).first()

    if existing_hours:
        existing_hours.open_time = opening_hours_create.open_time
        existing_hours.close_time = opening_hours_create.close_time
    else:
        opening_hours = models.OpeningHours(**opening_hours_create.dict(), restaurant_id=restaurant_id)
        db.add(opening_hours)

    db.commit()
    return db.query(models.Restaurant).options(joinedload(models.Restaurant.opening_hours)).filter(models.Restaurant.id == restaurant_id).first()

def get_restaurant_by_name(db: Session, restaurant_name: str) -> models.Restaurant:
    """Retrieve restaurant by its name."""
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_name).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Restaurant with name {restaurant_name} not found")
    return restaurant


def delete_restaurant(db: Session, restaurant_id: str):
    db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).delete()
    db.commit()

def get_all_restaurants(db: Session) -> List[models.Restaurant]:
    """Retrieve all restaurants in the database."""
    return db.query(models.Restaurant).all()

def get_restaurant_by_id(db: Session, restaurant_id: str) -> models.Restaurant:
    """Retrieve a restaurant by its ID."""
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()