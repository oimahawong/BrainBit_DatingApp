from google.cloud import storage

def upload_to_bucket(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client.from_service_account_json(
        r'halogen-inkwell-401500-65e54374e3c7.json')

    bucket = storage_client.bucket(bucket_name) # Get the bucket object
    blob = bucket.blob(destination_blob_name) # Create a blob object (this doesn't upload the file just yet)
    blob.upload_from_filename(source_file_name)     # Upload the file

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")