
# importing geopy library
from geopy.geocoders import Nominatim
 
def extract_lat_long_via_address(full_address):
    print(full_address)
    loc = Nominatim(user_agent="GetLoc")

    getLoc = loc.geocode(full_address)
    print(getLoc.latitude)
    return getLoc.latitude, getLoc.longitude

