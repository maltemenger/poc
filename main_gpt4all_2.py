from langchain.chains import RetrievalQA, LLMChain
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import GPT4All
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

loader = PyPDFLoader("data/entwicklungsrichtlinien.pdf")
docs = loader.load()

# split it into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
splitted_docs = text_splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

chroma_db = Chroma.from_documents(
    documents=splitted_docs,
    embedding=embeddings,
    persist_directory="data",
    collection_name="lc_chroma_demo2",
)

template = """
Verwende folgenden Kontext:
{context}
Bitte beantworte die Frage so gut wie möglich.

 - -
Frage: {question}
"""


query = "welche workshops werden von der Capgemini geplant und welchen Mehrwert haben die für die N-ergie?"

query = input("Frage eingeben: ")

similar_docs = chroma_db.similarity_search(query=query, k=5)


context = ""
for doc in similar_docs:
    context = context + doc.page_content + " \n\n "


gpt4all_path = "C:\ki\sim2\models\mistral-7b-openorca.Q4_0.gguf"
llm = GPT4All(model=gpt4all_path, n_threads=4)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=chroma_db.as_retriever())

prompt = PromptTemplate(
    template=template, input_variables=["context" "question"]
).partial(context=context)
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.invoke(query))
