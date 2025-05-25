from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from ollama import AsyncClient
from diskcache import Cache 



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
            chunk_overlap=60,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        self.cache = Cache("data/query_cache")

    def ingest_knowledge(self, text):
        docs = self.text_splitter.create_documents([text])
        self.vector_db.add_documents(docs)

    def retrieve_context(self, query):
        cache_key = f"query_{hash(query)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Original retrieval logic
        results = self.vector_db.similarity_search_with_score(query, k=1)
        filtered = [doc for doc, score in results if score < 0.4]  

        
        # Cache for 24 hours
        self.cache.set(cache_key, filtered, expire=86400)
        return filtered
    

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
    
     
