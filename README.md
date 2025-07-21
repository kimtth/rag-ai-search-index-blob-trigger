# Azure AI Search Indexer – Blob Triggered Azure Function

Azure Function with Blob Trigger to trigger indexing documents into Azure AI Search from Blob Storage.

### 🔧 Prerequisites

Ensure the following Azure roles are assigned to the identity running the function:

- <b>Trigger Storage Blob Data Owner</b> and <b>Storage Queue Data Contributor</b>

> 💡 [Learn more about the Blob Trigger for Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-trigger)

###  Deployment

Use the Azure Functions Core Tools to publish your Python function app:

```bash
func azure functionapp publish <your-func-app-name> --python
```
