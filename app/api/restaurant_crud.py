from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models import models
from app.schema import RestaurantSchema
from app.enums import search_enums

def create_restaurant(db: Session, restaurant: RestaurantSchema.RestaurantCreate):
    new_restaurant = models.Restaurant(name = restaurant.name, chef_name = restaurant.chef_name, 
                            cuisine = restaurant.cuisine, establishment_type = restaurant.establishment_type, address = restaurant.address, description = restaurant.description,
                            is_active = restaurant.is_active, open_now = restaurant.open_now)
    #breakpoint()
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

def get_restaurant_by_cuisine(db: Session, cuisine: search_enums.CuisineEnum):
    query = db.query(models.Restaurant).filter(cuisine == models.Restaurant.cuisine).first()
    #if query is None:
    #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                       detail=f"Restaurant with id {id} not found")
    return query

def get_restaurant_by_establishment_type(db: Session, establishemnt_type: str):
    query = db.query(models.Restaurant).filter(establishemnt_type == models.Restaurant.establishemnt_type).all()
    #if query is None:
    #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                       detail=f"Restaurant with id {id} not found")
    return query

def get_restaurant_id_by_name(db: Session, name: str):
    # Query the database to retrieve the business ID based on the business name
    query = db.query(models.Restaurant).filter(models.Restaurant.name == name).first()
    if query is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Restaurant with name {name} not found")
    return query

from sqlalchemy.orm import Session

# Function to add opening hours to a business
def add_opening_hours(db: Session, restaurant_id: str, opening_hours_create: RestaurantSchema.OpeningHoursCreate):
    # Ensure that the business with the specified ID exists
    query = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Restaurant with id {restaurant_id} not found")
    # Create an OpeningHours object based on the input data
    # ** is dereferecing the dictioanary and unpacking it 
    opening_hours = models.OpeningHours(**opening_hours_create.dict(), restaurant_id=restaurant_id)

    # Add the opening hours to the database
    db.add(opening_hours)
    db.commit()
    db.refresh(opening_hours)

    restaurant = db.query(models.Restaurant).options(joinedload(models.RestaurantResponse.opening_hours)).filter(models.Restaurant.id == restaurant_id).first()

    # Refresh the business to include the newly added opening hours

    return restaurant  # Return the updated business object with the new opening hours


