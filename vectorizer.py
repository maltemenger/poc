import json

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from models.chunk import Chunk


class Vectorizer:
    embeddings = HuggingFaceEmbeddings(
        model_name="danielheinz/e5-base-sts-en-de"
    )
    chroma_db = Chroma(persist_directory="./data", embedding_function=embeddings)


    def get_chunks(self, query, num_chunks):
        #similar_docs = self.chroma_db.similarity_search(query=query, k=num_chunks)
        similar_docs = self.chroma_db.similarity_search_with_score(query=query, k=num_chunks)
        all_docs = []

        for doc, score in similar_docs:
            chunk = Chunk(doc.page_content, doc.metadata["page"] + 1, doc.metadata["source"], score)
            all_docs.append(chunk)


        sorted_docs = sorted(all_docs, key=lambda doc: doc.score)

        return sorted_docs
