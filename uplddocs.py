import openai
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from typing import Any


search_endpoint = "https://indexsearch92.search.windows.net"
search_api_key = "F1AeyKKt14tvp5PAudk5da3RttgrgbRvAiSsGCIBuHAzSeASIGPL"
index_name = "indexsearch92"
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=AzureKeyCredential(search_api_key))


openai.api_type = "azure"
openai.api_base = "https://nwopnai92.openai.azure.com/" #deleted okay to post
openai.api_version = "2023-07-01-preview"
openai.api_key = "Azure_key"


documents = [
    {"id": "doc1", "content": "Attacker note blaming ransomware..."},
    {"id": "doc5", "content": "Root-Cause Analysis: Blue Raven exploit in SVR-ACME-01..."},
    
]


for doc in documents:
    response: Any = openai.Embedding.create(
        input=doc["content"],
        engine="embed-rag92"
    )

    embedding = response["data"][0]["embedding"]

    enriched_doc = {
        "id": doc["id"],
        "content": doc["content"],
        "contentVector": embedding
    }

    search_client.upload_documents(documents=[enriched_doc])
    print(f" Uploaded {doc['id']}")

print(" All documents embedded and uploaded.")

