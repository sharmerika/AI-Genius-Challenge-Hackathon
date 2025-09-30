import requests
import json

endpoint = "https://indexsearch92.search.windows.net"
api_key = "azure_key"

url = f"{endpoint}/indexes?api-version=2023-11-01"
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

index_schema = {
    "name": "indexsearch92",
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "searchable": False},
        {"name": "content", "type": "Edm.String", "searchable": True, "retrievable": True},
        {
            "name": "contentVector",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "retrievable": False,
            "dimensions": 1536,
            "vectorSearchConfiguration": "default"
        }
    ],
    "vectorSearch": {
        "algorithmConfigurations": [
            {"name": "default", "kind": "hnsw"}
        ]
    }
}


response = requests.post(url, headers=headers, data=json.dumps(index_schema))
print(response.status_code)
print(response.text)
