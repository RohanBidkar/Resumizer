
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from config import Config
import time
import os


class SimpleEmbeddings:
    
    def __init__(self):
        print("⚡ Loading embedding model (cached from Docker build)...")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("✅ Model ready!")
    
    def embed(self, text):
        """Create embedding for text"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts):
        """Create embeddings for multiple texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


class SimpleRAG:
    
    def __init__(self):
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        self.index_name = Config.PINECONE_INDEX_NAME
        self.embeddings = SimpleEmbeddings()
        
        # Skip index creation check in production to speed up cold starts
        # Set SKIP_INDEX_CHECK=true in Render environment variables
        skip_check = os.getenv("SKIP_INDEX_CHECK", "false").lower() == "true"
        
        if not skip_check:
            self._create_index_if_needed()
        else:
            print(f"⚡ Skipping index check (production mode)")
            
        self.index = self.pc.Index(self.index_name)
        print(f"✅ Connected to Pinecone: {self.index_name}")
    
    def _create_index_if_needed(self):
        existing = [idx.name for idx in self.pc.list_indexes()]
        
        if self.index_name not in existing:
            print(f"Creating index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # all-MiniLM-L6-v2 = 384 dimensions
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            time.sleep(3)
    
    def chunk_text(self, text):
        words = text.split()
        chunks = []
        chunk_size = 200
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def store_resume(self, resume_text, resume_id):
        chunks = self.chunk_text(resume_text)
        print(f"   Split into {len(chunks)} chunks")
        
        embeddings = self.embeddings.embed_batch(chunks)
        
        vectors = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{resume_id}_chunk_{idx}",
                "values": embedding,
                "metadata": {
                    "resume_id": resume_id,
                    "text": chunk,
                    "chunk_index": idx
                }
            })
        
        self.index.upsert(vectors=vectors)
        print(f"   ✅ Stored in Pinecone")
    
    def search(self, query, top_k=3):
        """Search for relevant chunks"""
        query_embedding = self.embeddings.embed(query)
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        matches = []
        for match in results.matches:
            matches.append({
                "text": match.metadata.get("text", ""),
                "score": match.score
            })
        
        return matches


# Global instances
_embeddings = None
_rag = None

def get_embeddings():
    """Get or create embeddings service"""
    global _embeddings
    if _embeddings is None:
        _embeddings = SimpleEmbeddings()
    return _embeddings

def get_rag():
    global _rag
    if _rag is None:
        _rag = SimpleRAG()
    return _rag
