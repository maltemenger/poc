from typing import Dict

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from database.chroma_config import ChromaConfig


class ChromaClient:
    def __init__(self):
        config = ChromaConfig()
        self.localChroma = Chroma(persist_directory="data", collection_name=config.collection_name, embedding_function=config.embeddings)

    def query_chroma(self, question: str) -> list[Document]:
        return self.localChroma.similarity_search(question)

    def similarity_search_with_score(self, query: str, num_chunks: int, filter_by_tag: Dict[str, str] = None):
        return self.localChroma.similarity_search_with_score(query=query, k=num_chunks, filter=filter_by_tag)

