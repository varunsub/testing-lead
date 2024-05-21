import os
from google.cloud import storage
from google.oauth2 import service_account


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    try:
        # Construct the credentials from environment variables
        credentials_info = {
            "type": os.environ["type"],
            "project_id": os.environ["project_id"],
            "private_key_id": os.environ["private_key_id"],
            "private_key": os.environ["private_key"].replace("\\n", "\n"),
            "client_email": os.environ["client_email"],
            "client_id": os.environ["client_id"],
            "auth_uri": os.environ["auth_uri"],
            "token_uri": os.environ["token_uri"],
            "auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
            "client_x509_cert_url": os.environ["client_x509_cert_url"],
        }

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )

        storage_client = storage.Client(
            credentials=credentials, project=os.environ["project_id"]
        )
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        return blob.public_url
    except Exception as e:
        print(e)
        return ""
