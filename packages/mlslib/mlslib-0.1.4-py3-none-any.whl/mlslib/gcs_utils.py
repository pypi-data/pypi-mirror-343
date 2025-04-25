import pandas as pd
import subprocess
import tempfile
import os
from google.cloud import storage

def download_csv(bucket_name: str, file_path: str) -> str:
    """
    Makes the specified file in GCS public and returns the HTTPS download link.
    
    Parameters:
        bucket_name (str): GCS bucket name
        file_path (str): Path inside the bucket (e.g., "folder/file.csv")

    Returns:
        str: HTTPS link to the file
    """
    gcs_uri = f"gs://{bucket_name}/{file_path}"

    # Make the file public using gsutil
    subprocess.run(["gsutil", "acl", "ch", "-u", "AllUsers:R", gcs_uri], check=True)

    # Generate public HTTPS link
    url = f"https://storage.googleapis.com/{bucket_name}/{file_path}"
    return url

def upload_df_to_gcs_csv(df: pd.DataFrame, bucket_name: str, gcs_path: str, project_id: str = None) -> str:
    """
    Save a DataFrame as a CSV file and upload it to a GCS bucket.

    Args:
        df (pd.DataFrame): The DataFrame to upload.
        bucket_name (str): GCS bucket name.
        gcs_path (str): Destination path in GCS (e.g., 'folder/file.csv').
        project_id (str, optional): GCP project ID for the storage client.

    Returns:
        str: Public or authenticated GCS path where the file was uploaded.
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        temp_path = tmp.name
    print(temp_path)

    # Upload to GCS
    client = storage.Client(project=project_id)
    print(client)
    bucket = client.bucket(bucket_name)
    print(bucket)
    blob = bucket.blob(gcs_path)
    print(blob)
    blob.upload_from_filename(temp_path)
    os.remove(temp_path)

    return f"gs://{bucket_name}/{gcs_path}"