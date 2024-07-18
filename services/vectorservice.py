from database.chroma_client import ChromaClient
from models.chunk import Chunk


class VectorService:
    @staticmethod
    def get_chunks(query: str, num_chunks: int) -> list[Chunk]:
        chroma = ChromaClient()
        similar_docs = chroma.similarity_search_with_score(query=query, num_chunks=num_chunks)
        all_docs = []

        for doc, score in similar_docs:
            if doc.metadata.get("page") is not None and doc.metadata.get("source") is not None:
                chunk = Chunk(doc.page_content, doc.metadata["page"] + 1, doc.metadata["source"], score)
                all_docs.append(chunk)
                print(doc.metadata["source"])

        sorted_docs = sorted(all_docs, key=lambda doc: doc.score)

        return sorted_docs
