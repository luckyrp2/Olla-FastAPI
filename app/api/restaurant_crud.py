from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Restaurant
from app.schema.RestaurantSchema import RestaurantBase

def create_restaurant(db: Session, restaurant: RestaurantBase):
    restaurant = Restaurant(id = restaurant.id,
                                    date_added = restaurant.date_added,
                                    name = restaurant.name,
                                    chef_name = restaurant.chef_name
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def get_restaurant_by_id(db: Session, id: int):
    query = db.query(Restaurant).filter(id == Restaurant.id).first()
    #if query is None:
    #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                       detail=f"Restaurant with id {id} not found")
    return query