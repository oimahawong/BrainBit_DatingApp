import os

from google.cloud import storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client.from_service_account_json(
        'tools/halogen-inkwell-401500-a4aa72be527e.json')

    bucket = storage_client.bucket(bucket_name) # Get the bucket object
    blob = bucket.blob(destination_blob_name) # Create a blob object (this doesn't upload the file just yet)
    blob.upload_from_filename(source_file_name)     # Upload the file

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def download_from_bucket(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client.from_service_account_json(
        'tools/halogen-inkwell-401500-a4aa72be527e.json')

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def download_all_from_bucket(bucket_name, destination_folder, prefix=""):
    storage_client = storage.Client.from_service_account_json('tools/halogen-inkwell-401500-a4aa72be527e.json')
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    blob_names = []
    for blob in blobs:
        if blob.name.endswith('/'):
            continue

        destination_file_name = os.path.join(destination_folder, blob.name.replace('/', os.sep))
        directory = os.path.dirname(destination_file_name)

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

        if not os.path.isfile(destination_file_name):
            blob.download_to_filename(destination_file_name)
            print(f"Downloaded blob to {destination_file_name}")

        if os.path.isfile(destination_file_name):
            print(f"File already exists: {destination_file_name}")



        blob_names.append(destination_file_name)

    return blob_names
