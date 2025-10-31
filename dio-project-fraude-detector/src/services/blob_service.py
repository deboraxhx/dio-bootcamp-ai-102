import os
import streamlit as st
from azure.storage.blob import BlobServiceClient
from utils.config import Config


def upload_file_to_blob(file, filename):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            Config.STORAGE_CONNECTION_STRING
        )
        container_client = blob_service_client.get_container_client(
            Config.CONTAINER_NAME
        )

        # Resetar o ponteiro do arquivo para o início
        file.seek(0)

        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file, overwrite=True)

        # Obter a URL real do blob
        blob_url = blob_client.url
        return blob_url

    except Exception as e:
        st.error(f"Erro ao enviar o arquivo para o Blob Storage: {e}")
        return None
