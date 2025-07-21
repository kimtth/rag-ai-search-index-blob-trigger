import azure.functions as func
import logging
import azurefunctions.extensions.bindings.blob as blob

from push_aisearch_doc import AISearchPushIndex

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
CONTAINER_NAME = "faq-blob"
CSV_FILE_NAME = "faq.csv"

@app.blob_trigger(
    arg_name="blob_client", path=f"{CONTAINER_NAME}/{CSV_FILE_NAME}", connection="AZURE_SEARCH_STORAGE_CONNECTION"
)
def blob_trigger_to_search_index(blob_client: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Properties: {blob_client.get_blob_properties()}\n"
        f"Blob content head: {blob_client.download_blob().read(size=1)}"
    )

    try:
        # download entire blob into memory
        data = blob_client.download_blob().readall()
        logging.info(f"Blob size: {len(data)} bytes")
        # push to Azure AI Search
        aisearch_push_index = AISearchPushIndex()
        aisearch_push_index.run(data)
    except Exception as e:
        logging.error(f"Error processing blob: {e}")
        raise
