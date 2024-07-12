from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain_community.llms import GPT4All


class InternalGPT:

    def answer_question(self, query):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        chroma_db = Chroma(persist_directory="./data", embedding_function=embeddings)

#        template = """
#       ### System:
#        Verwende für deine Antwort folgenden Kontext:
#        {context}
#
#        Verwende dabei nur die Informationen aus deinem Kontext.
#        Du darfst auf keine Informationen zugreifen, die nicht im Kontext sind.
#        Gebe hinter deiner Antwort immer eine Quellenangabe und Seitenangabe.
#        Beantworte keine Fragen, wenn du in deinem Kontext keine Antwort findest.
#
#         - -
#        Frage: {question}
#        """

        template = """
        Use only the information in the context to generate your answer:
        {context}
        You are not allowed to access information that is not in the context. Always add references to the document 
        and the page number that were used to generate the answer at the end of your answer. Dont answer if you dont have information about the question in your
        context. Answer only in german.
        
        --
        Question: {question}
        
        """
        print("QUERY")
        print(query)
        similar_docs = chroma_db.similarity_search(query=query, k=2)

        context = ""
        for doc in similar_docs:
            context = context + doc.page_content + " Seite: " + str(doc.metadata["page"]) + ". Quelle: " + doc.metadata["source"] + " \n\n "


        print("!!!!!!!!!!!!! Context:")
        print(context)
        print("!!!!!!!!!!!!!! Endcontext!")

        gpt4all_path = "C:\ki\sim2\models\mistral-7b-openorca.Q4_0.gguf"
        llm = GPT4All(model=gpt4all_path, n_threads=4)

        prompt = PromptTemplate(
            template=template, input_variables=["context" "question"]
        ).partial(context=context)

        llm_chain = LLMChain(prompt=prompt, llm=llm)
        print("Start model")
        answer = llm_chain.invoke(query)
        return answer