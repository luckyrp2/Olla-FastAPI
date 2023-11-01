# SDK initialization
from imagekitio import ImageKit

from imagekitio.models.ListAndSearchFileRequestOptions import ListAndSearchFileRequestOptions

imagekit = ImageKit(
    private_key='private_C9/9aNTYl4byjBsIGjg8eBLKhIY=',
    public_key='public_iIZx9Ab1gSlbjZ6b36e+r2XRhSE=',
    url_endpoint='https://ik.imagekit.io/olla'
)

def get_card_image_url(name, dish):
    url_endpoint='https://ik.imagekit.io/olla'
    restaurant_file_path = "/" + name + " - " + dish
    url = url_endpoint + "/" + restaurant_file_path + "/Image/Cover Image"
    url_1 = restaurant_file_path + "/Image/Cover Image"
    url_2 = f'olla/Restaurant%20Name%20-%20Dish%20Name/Image/Cover%20Image/'
    print(url_2)
    list_files = imagekit.list_files(options=ListAndSearchFileRequestOptions(path=url_2))
    
    print(list_files.response_metadata.raw)

def get_video_url(name, dish):
    url_endpoint='https://ik.imagekit.io/olla'
    restaurant_file_path = name + " - " + dish
    url = url_endpoint + "/" + restaurant_file_path + "/Image/Cover Image"
    print(url)
    

def get_video_url(name, dish):
    url_endpoint='https://ik.imagekit.io/olla'
    restaurant_file_path = name + " - " + dish
    url = url_endpoint + "/" + restaurant_file_path + "/Video"
    print(url)


get_card_image_url("Restaurant", "Dish")