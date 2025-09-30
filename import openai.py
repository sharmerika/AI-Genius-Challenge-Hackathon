import openai
from typing import Any

openai.api_type = "azure"
openai.api_base = "https://nwopnai92.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "azure_key"

response: Any = openai.Embedding.create(
    input="Test embedding",
    engine="embed-rag92"
)

embedding = response['data'][0]['embedding']
print(embedding[:5])

