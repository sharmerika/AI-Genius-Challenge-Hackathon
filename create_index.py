import azure.search.documents.indexes.models as models
print(dir(models))

from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    VectorSearchAlgorithmConfiguration
)

from azure.core.credentials import AzureKeyCredential


endpoint = "https://indexsearch92.search.windows.net" #okay to post they were deleted
api_key = "Azure_key"


client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))


index_name = "indexsearch92"
fields = [
    SimpleField(name="id", type="Edm.String", key=True),
    SearchableField(name="content", type="Edm.String"),
    SimpleField(
        name="contentVector",
        type="Collection(Edm.Single)",
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="default"
    )
]

vector_search = VectorSearch(
    profiles=[
        VectorSearchProfile(
            name="default",
            algorithm_configuration_name="default"
        )
    ],
    algorithm_configurations=[
        VectorSearchAlgorithmConfiguration(
            name="default",
            kind="hnsw"
        )
    ]
)


index = SearchIndex(
    name=index_name,
    fields=fields,
    vector_search=vector_search
)


try:
    client.create_index(index)
    print(f" Index '{index_name}' created successfully.")
except Exception as e:
    print(f" Error creating index: {e}")