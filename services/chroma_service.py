from typing import Dict

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from models.chroma_client import ChromaClient
from database.chroma_config import ChromaConfig
from models.chunk import Chunk


class ChromaService:
    def add_tags(self, item: Document, tag: str):
        item.metadata['tag'] = tag
        return item

    def add_document(self, document_path: str, tag: str):
        print(f"Add Document - {document_path} with tag {tag}")
        loader = PyPDFLoader(document_path)
        docs = loader.load()
        docs_with_metadata = list(map(lambda x: self.add_tags(x, tag), docs))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2400, chunk_overlap=200)
        splitted_docs = text_splitter.split_documents(docs_with_metadata)

        config = ChromaConfig()

        Chroma.from_documents(
            documents=splitted_docs,
            embedding=config.embeddings,
            collection_name=config.collection_name,
            persist_directory=config.persist_directory
        )
        print('Finished adding Document')

    @staticmethod
    def get_chunks(query: str, num_chunks: int, filter_by_tag: Dict[str, str] = None) -> list[Chunk]:
        chroma = ChromaClient()
        similar_docs = chroma.similarity_search_with_score(query=query,
                                                           num_chunks=num_chunks,
                                                           filter_by_tag=filter_by_tag)
        all_docs = []

        for doc, score in similar_docs:
            if doc.metadata.get("page") is not None and doc.metadata.get("source") is not None:
                chunk = Chunk(doc.page_content, doc.metadata["page"] + 1, doc.metadata["source"], score)
                all_docs.append(chunk)
                print(doc.metadata["source"])

        sorted_docs = sorted(all_docs, key=lambda doc: doc.score)

        return sorted_docs

