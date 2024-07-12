class Chunk:
    def __init__(self, content, page, source_doc, score):
        self.content = content
        self.page = page
        self.source_doc = source_doc
        self.score = score

    def __repr__(self):
        return f"Document(content={self.content}, page={self.page}, source_doc={self.source_doc}, {self.score})"

