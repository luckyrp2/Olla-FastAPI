from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import models
from app.schema import RestaurantSchema

def create_restaurant(db: Session, restaurant: RestaurantSchema.RestaurantCreate):
    restaurant = RestaurantSchema.RestaurantCreate(name = restaurant.name, chef_name = restaurant.chef_name, 
                            address = restaurant.address, description= restaurant.description,
                            is_active= restaurant.is_active)
    
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def get_restaurant_by_id(db: Session, id: int):
    query = db.query(models.Restaurant).filter(id == models.Restaurant.id).first()
    #if query is None:
    #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                       detail=f"Restaurant with id {id} not found")
    return query