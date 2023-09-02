from celery import shared_task
from .bucket import bucket


@shared_task
def upload_object_task(file_path ,object_name):
    bucket.upload_object(file_path ,object_name)



@shared_task
def delete_object_task(object_name):
    return bucket.delete_object(object_name)

@shared_task
def download_object_task(object_name):
    return bucket.download_object(object_name)