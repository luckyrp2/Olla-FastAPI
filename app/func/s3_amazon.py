import boto3
import pandas
from enum import Enum 

class FileType(Enum): 
   filler_photos = "Additional Images"
   card_photo_file_path = "Cover Image"
   podcast_file_path = "Podcast"
   video_file_path = "Video"
 
s3_client = boto3.client(
    's3',
    aws_access_key_id = 'AKIA5OWZ6EO72UBER3ZB',
    aws_secret_access_key = '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',
    region_name = 'us-west-1'
)


def get_content(restaurant_name, dish_name, path):
   bucket_name = 'olla-media' 
   path_type = path.value
   prefix = restaurant_name + '/' + dish_name + '/' + path_type 
   response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
   files = response.get("Contents")
   url_list = []
   if files is None:
      url_list.append(None)
   else:
      for file in files[1:]:
         path = file['Key']

         url = s3_client.generate_presigned_url(
                     ClientMethod='get_object',
                     Params={'Bucket': bucket_name, 'Key': path, },
                     ExpiresIn=600000,
                  )
         
         url_list.append(url)
   return url_list
