import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="contracts",
    embedding_function=embedding_fn
)
