# chroma_config.py

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings


class ChromaConfig:
    embeddings: Embeddings = HuggingFaceEmbeddings(
        model_name="danielheinz/e5-base-sts-en-de"
    )
    persist_directory = "./data"
    collection_name = "ubahn"
