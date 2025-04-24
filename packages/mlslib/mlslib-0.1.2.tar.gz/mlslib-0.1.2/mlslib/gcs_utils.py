import subprocess

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
