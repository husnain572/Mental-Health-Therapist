# backend/rag_engine.py
import os
import random
import chromadb

class RAGEngine:
    def __init__(self, kb_path="backend/knowledge_base/mental_health_tips.txt"):
        self.client = chromadb.Client()

        # Use existing collection if present
        existing = self.client.list_collections()
        if any(c.name == "mh_tips" for c in existing):
            self.collection = self.client.get_collection("mh_tips")
        else:
            self.collection = self.client.create_collection(name="mh_tips")

        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"{kb_path} not found.")

        with open(kb_path, "r", encoding="utf-8") as f:
            self.docs = [line.strip() for line in f.readlines()]

        # Add docs to ChromaDB with dummy embeddings
        if self.collection.count() == 0:
            for idx, doc in enumerate(self.docs):
                self.collection.add(
                    ids=[str(idx)],
                    embeddings=[[0]*384],  # dummy embedding
                    documents=[doc]
                )

    def search(self, query: str, top_k=1):
        # Return a random tip instead of real embedding search
        return random.choice(self.docs)
