from typing import Optional

import chromadb
from chromadb import Settings, ClientAPI, Embeddings
from langchain_community.vectorstores import Chroma


class ChromaClient:
    def __init__(self, collection_name: str, embeddings: Optional[Embeddings] = None):
        client = chromadb.HttpClient(settings=Settings(allow_reset=True))
        self.chroma = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )

    def query_chroma(self, question: str):
        docs = self.chroma.similarity_search(question)
        print(docs[0].page_content)