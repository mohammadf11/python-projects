import boto3
import logging
from botocore.exceptions import ClientError
from config import settings
logging.basicConfig(level=logging.INFO)
class Bucket:

    def __init__(self) -> None:
        try:
            resource = boto3.resource(
                service_name = settings.AWS_SERVICE_NAME,
                endpoint_url = settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id =    settings.AWS_S3_ACCESS_KEY_ID,
                aws_secret_access_key =settings.AWS_S3_SECRET_ACCESS_KEY,
            )
            self.download_path = settings.AWS_LOCAL_STORAGE
            self.bucket = resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        except Exception as exc:
            logging.error(exc)


    def upload_object(self , file_path ,object_name):
        try:
            with open(file_path, "rb") as file:
                self.bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
            return True
        except ClientError as e:
            logging.error(e)

    def delete_object(self , object_name):
        try:
            object = self.bucket.Object(object_name)
            return object.delete()
        except ClientError as e:
            logging.error(e)


    def download_object(self , object_name):
        try: 
            self.bucket.download_file(
                object_name,
                f'{self.download_path}/{object_name}',
            )
            return True
        except ClientError as e:
            logging.error(e)


bucket = Bucket()
