import os
import ollama
import utils
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever


MODEL = "llama3.2"
CHROMA_DB_DIR = "./db"
LLM = ChatOllama(model=MODEL)
PATH_ADD_DOC = "./to-add"
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an assistant for developers. Your task is to generate a simple 
    answer of the relevant documents you have in your a vector database. 
    By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)


def finish_chat():
    print("Chat finished by user")


def add_document():
    if utils.is_empty_directory(PATH_ADD_DOC):
        print("\033[93mNothing to add.\033[0m\n")
        return
        
    files = os.listdir(PATH_ADD_DOC)

    for file in files:
        if utils.is_document_added(file):
            print(f"Remove document {file} from base_de_documentos.txt. This file was already added to {MODEL}.\n")
            return

    vector_db = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag"
    )

    for file in files:
        loader = UnstructuredPDFLoader(file_path=f"./{PATH_ADD_DOC}/{file}")
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
        chunks = splitter.split_documents(pages)
        ollama.pull("nomic-embed-text")
        
        vector_db.add_documents(chunks)
        utils.write_document_name(file)
    
    print("arquivos adicionados")


def chat_llm():
    if not utils.is_directory(CHROMA_DB_DIR):
        print("\033[93mNo documents added to database.\033[0m\n")
        return
    
    print("Loading documents...")
    vector_db = Chroma(
        embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag",
        persist_directory=CHROMA_DB_DIR
    )
    ollama.pull("nomic-embed-text")

    retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), LLM, prompt=QUERY_PROMPT
    )

    while True:
        template = """Answer the question based ONLY on the following context: {context}
        Question: {question} """
        
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | LLM
            | StrOutputParser()
        )

        user_prompt = input("Me: ")
        if "-exit" in user_prompt:
            finish_chat()
            return
                
        llm_response = chain.invoke(input=(user_prompt,))
        print(f"\nOllama: {llm_response}\n")


def main():
    while True:
        opt = utils.read_option("1- Conversar com o Assitente\n2- Adicionar documento\n3- Sair\nDigite sua opção: ", 3)
        match opt:
            case 1: chat_llm()
            case 2: add_document()
            case 3: break
            case _: continue
    finish_chat()

if __name__ == "__main__":
    main()
