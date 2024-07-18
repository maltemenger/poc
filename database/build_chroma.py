from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from database.chroma_config import ChromaConfig


class ChromaService:
    def add_tags(self, item: Document, tag: str):
        item.metadata['tag'] = tag
        return item
    def build_chroma_from_document(self, document_path: str, tag: str):
        print('Building Chroma')
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
        print('Finished building Chroma')




newChroma = ChromaService()
newChroma.build_chroma_from_document('../data/g1.pdf', 'g1')
