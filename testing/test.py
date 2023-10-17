import requests
import json



res = {'name': 'xyz', 'chef_name': 'Bob', 'address': '21484 Continental Circle', 'description': 'hello',
       'is_active': True}


response = requests.post('http://127.0.0.1:8000/restaurant/new', data=res)

print(response.json())