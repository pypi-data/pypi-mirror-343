"""
This module provides a simple wrapper for interacting with Azure Blob Storage containers.
It defines the AzsContainerClient class, which allows you to upload and download blobs
using either a connection string or a SAS URL.
"""

from azure.storage.blob import BlobServiceClient, ContainerClient, ContentSettings
import logging
import os
from pathlib import Path
from azure.core.exceptions import ResourceExistsError, HttpResponseError, ResourceNotFoundError

logger = logging.getLogger("mpf-utils.azstorage")


class AzsContainerClient:
    """
    A client for interacting with an Azure Blob Storage container.

    This class allows uploading and downloading blobs from an Azure Storage container.
    It can establish the connection using either a connection string (with a specified container)
    or a SAS (Shared Access Signature) URL.
    """

    def __init__(self, container_name: str = None, conn_str: str = None, sas_url: str = None):
        """
        Initialize the AzsContainerClient.

        Parameters:
            container_name (str, optional): The name of the container. This is required when using a connection string.
            conn_str (str, optional): The connection string for the Azure Storage account.
                If not provided, the connection string will be fetched from the environment variable 'MPFU_AZSTORAGE_CONNECTION_STRING'.
            sas_url (str, optional): The SAS URL for the container. If provided, it overrides the connection string.

        Notes:
            - If neither 'conn_str' nor 'sas_url' is provided, the connection string is obtained from the environment.
            - The SAS URL, if provided, takes precedence over the connection string.
        """
        if not conn_str and not sas_url:
            conn_str = os.getenv("MPFU_AZSTORAGE_CONNECTION_STRING")
        
        if not sas_url:
            logger.info("Using connection string to connect to Azure Storage")
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            self.container_client = blob_service_client.get_container_client(container_name)
        else:
            # If a sas_url is provided, it overrides the connection string.
            logger.info("Using SAS URL to connect to Azure Storage")
            self.container_client = ContainerClient.from_container_url(sas_url)
        
    def upload_blob(self, blob_name, data, overwrite=True, content_type=None):
        """
        Upload data to a blob within the container.

        Parameters:
            blob_name (str): The name of the blob to be created or overwritten.
            data (bytes or str): The data to upload to the blob.
            overwrite (bool, optional): Whether to overwrite an existing blob with the same name. Defaults to True.
            content_type (str, optional): The content type of the blob. Defaults to None.

        Returns:
            str: The URL of the uploaded blob.

        """
        if content_type is None:
            content_type = "application/octet-stream" if isinstance(data, bytes) else "text/plain"

        blob_client = self.container_client.get_blob_client(blob=blob_name)
        blob_client.upload_blob(data, overwrite=overwrite, content_settings=ContentSettings(content_type=content_type))
        return blob_client.url



    def download_blob(self,
                  blob_name: str,
                  dest_path: str | Path | None = None,
                  *,
                  max_concurrency: int = 4) -> Path:
        """
        Download *blob_name* from this container and save it to *dest_path*.

        Parameters
        ----------
        blob_name : str
            Name of the blob in Azure Storage (e.g. "reports/2025-Q1.csv").
        dest_path : str | Path | None, optional
            Where to save the file locally.  If None (default) the blob is written
            to `Path.cwd() / Path(blob_name).name` – i.e. the current directory
            under its leaf-filename.
        max_concurrency : int, optional
            Parallel range-GET requests used by the SDK.  Increase for faster
            transfers on high-bandwidth links.

        Returns
        -------
        pathlib.Path
            The absolute path of the file that was written.

        Raises
        ------
        ResourceNotFoundError
            If the blob does not exist.
        HttpResponseError
            For other I/O or network-level failures.
        """
        # Determine local destination
        if dest_path is None:
            dest_path = Path.cwd() / Path(blob_name).name
        else:
            dest_path = Path(dest_path)

        dest_path.parent.mkdir(parents=True, exist_ok=True)  # ensure directory

        # Stream the blob directly into the file
        blob_client = self.container_client.get_blob_client(blob_name)
        downloader = blob_client.download_blob(max_concurrency=max_concurrency)

        with dest_path.open("wb") as fh:
            downloader.readinto(fh)

        return dest_path


    def list_blobs(self, prefix=None, include=None):
        """
        List blobs in the container.

        Parameters:
            prefix (str, optional): The prefix to filter blobs by name.
            include (list, optional): Additional properties to include in the listing.

        Returns:
            list: A list of blob names in the container.

        """
        blobs = self.container_client.list_blobs(name_starts_with=prefix, include=include)
        return blobs

    def get_blob_url(self, blob_name):
        """
        Get the URL of a blob in the container.

        Parameters:
            blob_name (str): The name of the blob.

        Returns:
            str: The URL of the blob.
        """
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        return blob_client.url

    def delete_blob(self, blob_name):
        """
        Delete a blob from the container.

        Parameters:
            blob_name (str): The name of the blob to delete.

        Returns:
            None
        """
        blob_client = self.container_client.get_blob_client(blob=blob_name)

        blob_client.delete_blob()

    def blob_exists(self, blob_name):
        """
        Check if a blob exists in the container.

        Parameters:
            blob_name (str): The name of the blob.

        Returns:
            bool: True if the blob exists, False otherwise.
        """
        return self.container_client.get_blob_client(blob=blob_name).exists()
            
        

        
