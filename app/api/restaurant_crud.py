from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from sqlalchemy import func

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

    new_address = models.Address(
        street=restaurant.address.street,
        city=restaurant.address.city,
        great_city=restaurant.address.great_city,
        state=restaurant.address.state,
        zipcode=restaurant.address.zipcode
        # add any other fields from the Address schema here
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    new_restaurant = models.Restaurant(
        name=restaurant.name,
        chef_name=restaurant.chef_name,
        cuisine=restaurant.cuisine,
        instagram=restaurant.instagram,
        menu=restaurant.menu,
        establishment_type=restaurant.establishment_type,
        address=new_address,
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

def get_restaurants_by_greater_city(db: Session, greater_city: str) -> List[models.Restaurant]:
    """Retrieve all restaurants in a given greater city area."""
    return db.query(models.Restaurant)\
             .filter(models.Restaurant.address.has(models.Address.great_city == greater_city))\
             .all()

from typing import List

def update_missing_lat_lon(db: Session) -> List[RestaurantSchema.RestaurantLocationUpdate]:
    # Query for all restaurants with NULL lat and lon in their associated addresses
    null_locations = db.query(models.Restaurant).join(models.Address).filter(models.Address.lat.is_(None), models.Address.lon.is_(None)).all()

    updated_names = []  # Store names of restaurants that will be updated

    for restaurant in null_locations:
        # Construct the address string
        address_string = f"{restaurant.address.street} {restaurant.address.city} {restaurant.address.state} {restaurant.address.zipcode}"
        
        lat, lon = geo_location.extract_lat_long_via_address(address_string)
        restaurant.address.lat = lat
        restaurant.address.lon = lon
        updated_names.append(restaurant.name)

    db.commit()

    # Now, retrieve updated latitude and longitude for the restaurants
    updated_restaurants = db.query(models.Restaurant.name, models.Address.lat, models.Address.lon).join(models.Address).filter(models.Restaurant.name.in_(updated_names)).all()
    
    # Convert the result to the Pydantic model
    result = [RestaurantSchema.RestaurantLocationUpdate(name=name, lat=lat, lon=lon) for name, lat, lon in updated_restaurants]
    return result

# In restaurant_crud.py or wherever your CRUD functions are defined

# In restaurant_crud.py or wherever your CRUD functions are defined

from datetime import datetime, time

def get_open_restaurants(db: Session, day_of_week: int, current_time_str: str) -> List[str]:
    
    # Try converting the string to a time object
    try:
        current_time = datetime.strptime(current_time_str, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Time {current_time_str} is not in the correct format HH:MM")

    open_restaurants = (
        db.query(models.Restaurant.id)
        .join(models.OpeningHours)
        .filter(
            models.OpeningHours.day_of_week == day_of_week,
            func.time(models.OpeningHours.open_time) <= current_time,
            func.time(models.OpeningHours.close_time) > current_time
        )
        .all()
    )

    # Extract the list of restaurant IDs
    restaurant_ids = [restaurant.id for restaurant in open_restaurants]

    # Update the 'open_now' status for these restaurants
    db.query(models.Restaurant).filter(models.Restaurant.id.in_(restaurant_ids)).update({models.Restaurant.open_now: search_enums.OpenNowEnum.OPEN.value}, synchronize_session=False)
    db.commit()

    return restaurant_ids

def update_restaurant_by_name(db: Session, restaurant_name: str, update_data: dict):
    # Find the restaurant by name
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant_name).first()
    if not restaurant:
        return None

    for key, value in update_data.items():
        if key == 'address':
            if restaurant.address:
                # Check if the address data is different from the current address
                address_changed = any(getattr(restaurant.address, k) != v for k, v in value.items())
                if address_changed:
                    # Update fields of the existing address
                    for addr_key, addr_value in value.items():
                        setattr(restaurant.address, addr_key, addr_value)
            else:
                # Create a new Address if none exists
                restaurant.address = models.Address(**value)
        else:
            setattr(restaurant, key, value)  # Regular attribute

    db.commit()
    return restaurant


def delete_inactive_restaurants(db: Session):
    # Find all inactive restaurants
    inactive_restaurants = db.query(models.Restaurant).filter(models.Restaurant.is_active == False).all()

    for restaurant in inactive_restaurants:
        # Delete associated dishes
        db.query(models.Dish).filter(models.Dish.restaurant_id == restaurant.id).delete()
        # Delete the restaurant
        db.delete(restaurant)

    db.commit()
    return len(inactive_restaurants)  # Return the count of deleted restaurants
