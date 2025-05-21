from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from ollama import AsyncClient 



class Brain:
    def __init__(self):

        self.embeddings = OllamaEmbeddings(model="all-minilm:l6-v2")
        self.client=AsyncClient()

        self.vector_db = Chroma(
            persist_directory="data/chroma_db",
            embedding_function=self.embeddings,
            client_settings=chromadb.Settings(
                anonymized_telemetry=False,
                allow_reset=False,
                is_persistent=True
            )

        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

    def ingest_knowledge(self, text):
        docs = self.text_splitter.create_documents([text])
        self.vector_db.add_documents(docs)

    def retrieve_context(self, query):
        return self.vector_db.similarity_search(query, k=3)
    

    async def summarize_context(self, context: str) -> str:
        prompt = f"""
Summarize the following philosophical background/context into 1-2 sentences:

{context}
"""
        response = await self.client.generate(
            model="gemma3:4b",
            prompt=prompt,
            options={"temperature": 0.3, "num_predict": 100}
        )
        return response["response"].strip()
    
     
