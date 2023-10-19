import enum

class CuisineEnum(enum.Enum):
    japan = "Japanese"
    thai = "Thai"
    chinese = "Chinese"
    italian = "Italian"
    american = "American"
    cuban = "Cuban"
    greek = "Greek"
    indian = "Indian"
    korean = "Korean"
    mexican = "Mexican"
    vietnamese = "Vietnamese"
    fusion = "Fusion"

class DietEnum(enum.Enum):
    vegan = "Vegan"
    vegetarian = "Vegetarian"
    pescetarian = "Pescetarian"
    gluten_free = "Gluten Free"

class FoodTypeEnum(enum.Enum):
    pizza = "Pizza"
    fries = "Fries"
    tacos = "Tacos"
    quesadilla = "Quesadilla"
    fried_chicken = "Fried Chicken"
    soup = "Soup"
    sushi = "Sushi"
    burrito = "Burrito"
    boba = "Boba"
    ice_cream = "Ice Cream"
    bread = "Bread"
    burger = "Burger"
    wings = "Wings"
    bagel = "Bagel"
    fried_rice = "Fried_Rice"
    coffee = "Coffee"
    matcha = "Matcha"

class EstablishmentTypeEnum(enum.Enum):
    restaurant = "Restaurant"
    bakery = "Bakery"
    ice_cream_shop = "Ice Cream Shop"
    coffee_shop = "Coffee Shop"
    grocery = "Grocery Store"
    food_truck = "Food Truck"
    farmers_market = "Farmers Market"


class OpenNowEnum(enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class DayOfWeekEnum(enum.Enum):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'


    










