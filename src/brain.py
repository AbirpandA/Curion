from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb



class Brain:
    def __init__(self):

        self.embeddings = OllamaEmbeddings(model="all-minilm:l6-v2")

        self.vector_db = Chroma(
            persist_directory="data/chroma_db",
            embedding_function=self.embeddings,
            client_settings=chromadb.Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )

        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def ingest_knowledge(self, text):
        docs = self.text_splitter.create_documents([text])
        self.vector_db.add_documents(docs)

    def retrieve_context(self, query):
        return self.vector_db.similarity_search(query, k=3)
    
     
