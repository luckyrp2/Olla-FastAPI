import requests

'''
Using Free Geocoding API: https://geocode.maps.co/

'''
GOOGLE_API_KEY = 'AIzaSyDljReU4P9vT3nOBybBkJPfVwV3kRoiwLo' 

def extract_lat_long_via_address(address_or_zipcode):
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://geocode.maps.co/search?q="
    endpoint = f"{base_url}={address_or_zipcode}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)

    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()[0]
        #address = results['display_name']
        lat = results['lat']
        lon = results['lon']
    except:
        return "Address could not be found"
    return lat, lon

