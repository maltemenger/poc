from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from database.chroma_config import ChromaConfig

print('Scanne Dokument ein.')
loader = PyPDFLoader("../data/g1.pdf")
docs = loader.load()

docs[0].metadata['tag'] = 'g1'

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
splitted_docs = text_splitter.split_documents(docs)
print(splitted_docs[0])

config = ChromaConfig()

embeddings = HuggingFaceEmbeddings(
    model_name="danielheinz/e5-base-sts-en-de"
)

print("Befülle ChromaDb.")
chroma_db = Chroma.from_documents(
    documents=splitted_docs,
    embedding=config.embeddings,
    collection_name=config.collection_name,
    persist_directory=config.persist_directory
    )

print("Vectorisierung abgeschlossen.")
