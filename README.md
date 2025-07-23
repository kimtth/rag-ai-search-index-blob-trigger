# Azure AI Search Indexer – Blob Triggered Azure Function

Azure Function with Blob Trigger to trigger indexing documents into Azure AI Search from Blob Storage.

### 🔧 Prerequisites

Select option 1 or 2 based on your scenario.

1. Access the blob container by `Access key`

    - The value assigned to `connection="AzureWebJobsStorage"` should be updated to the production connection string if you used Azurelite locally.

2. Access the blob container by `Managed Identity`

    > Ensure the following Azure roles are assigned to the identity running the function:

    - Naviagte to Storage Account IAM.
    - Assign <b>Storage Blob Data Owner</b> and <b>Storage Queue Data Contributor</b> to the function.
    - Added environment variables with ServiceUri as postfix to the function: `<CONNECTION_NAME_PREFIX>__blobServiceUri` & `<CONNECTION_NAME_PREFIX>__queueServiceUri`. The sample uses `AZURE_SEARCH_STORAGE` as the value for `<CONNECTION_NAME_PREFIX>`.
    - 🤔 Despite of settings, it still requires enabling `Allow storage account key access`: Singleton lock renewal failed for blob '.../host' with error code 403: KeyBasedAuthenticationNotPermitted. 

    > 💡 [Learn more about the Blob Trigger for Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-trigger)

###  Deployment

Use the Azure Functions Core Tools to publish your Python function app:

```bash
func azure functionapp publish <your-func-app-name> --python
```
