import io
import logging
import os
import csv
import time
import uuid
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

class AISearchPushIndex:
    def __init__(self):
        load_dotenv()
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_KEY")
        self.search_index = os.getenv("AZURE_SEARCH_INDEX_NAME")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_NAME")
        self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")

        self.openai_client = AzureOpenAI(
            azure_endpoint=self.openai_endpoint,
            api_key=self.openai_key,
            api_version=self.openai_api_version
        )
        self.search_client = SearchClient(
            endpoint=self.search_endpoint,
            index_name=self.search_index,
            credential=AzureKeyCredential(self.search_key)
        )

    def _read_rows(self, data: bytes) -> list[dict]:
        text_stream = io.StringIO(data.decode("utf-8"))
        return list(csv.DictReader(text_stream))

    def _create_embedded_docs(self, rows: list[dict]) -> list[dict]:
        docs, start = [], time.time()
        for row in rows:
            resp = self.openai_client.embeddings.create(
                input=row["question"],
                model=self.embedding_model
            )
            vector = resp.data[0].embedding
            if vector:
                docs.append({
                    "id": str(uuid.uuid4()),
                    "question": row["question"],
                    "answer": row["answer"],
                    "vector": vector
                })
        logging.info(f"Embedding generation time: {time.time() - start:.3f} seconds")
        return docs

    def generate_documents(self, data: bytes) -> list[dict]:
        rows = self._read_rows(data)
        return self._create_embedded_docs(rows)

    def index_documents(self, documents: list[dict]):
        result = self.search_client.merge_or_upload_documents(documents=documents)
        logging.info(f"Indexed {len(documents)} documents, result: {result}")

    def run(self, data: bytes):
        docs = self.generate_documents(data)
        if docs:
            self.index_documents(docs)
        else:
            logging.warning("No documents to index.")


