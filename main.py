from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter

loader = PyPDFLoader("data/strom.pdf")
docs = loader.load_and_split()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
splitted_docs = text_splitter.split_documents(docs)

llm = ChatOpenAI(model_name="gpt-4", temperature=0)
embeddings = OpenAIEmbeddings()

chroma_db = Chroma.from_documents(
    documents=splitted_docs,
    embedding=embeddings,
    persist_directory="data",
    collection_name="lc_chroma_demo"
)


query = "Wie lang ist die Vertragslaufzeit eines Strom Purnatur-Vertrags?"

docs = chroma_db.similarity_search(
    query=query,
    k=2
)

prompt_template = """Bitte Antworte kurz und prägnant 
{context}
"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)


chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=chroma_db.as_retriever(),
                                    return_source_documents=True,
                                    chain_type_kwargs={
                                            "prompt": prompt
                                        },
                                    )

response = chain(query)

print(response['result'])