import os

from google.cloud import storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client.from_service_account_json(
        r'halogen-inkwell-401500-65e54374e3c7.json')

    bucket = storage_client.bucket(bucket_name) # Get the bucket object
    blob = bucket.blob(destination_blob_name) # Create a blob object (this doesn't upload the file just yet)
    blob.upload_from_filename(source_file_name)     # Upload the file

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def download_from_bucket(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client.from_service_account_json(
        'tools/halogen-inkwell-401500-65e54374e3c7.json')

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def download_all_from_bucket(bucket_name, destination_folder):
    storage_client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-65e54374e3c7.json')

    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    blob_names = []
    for blob in blobs:
        destination_file_name = os.path.join(destination_folder, blob.name)
        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
        blob.download_to_filename(destination_file_name)
        blob_names.append(destination_file_name)
        print(f"Blob {blob.name} downloaded to {destination_file_name}")
    return blob_names