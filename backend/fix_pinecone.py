"""
Script to recreate Pinecone index for simplified version
New dimension: 384 (HuggingFace all-MiniLM-L6-v2)
"""

from pinecone import Pinecone, ServerlessSpec
from config import Config
import time

def recreate_index():
    print("🔧 Recreating Pinecone index for simplified version...")
    
    pc = Pinecone(api_key=Config.PINECONE_API_KEY)
    index_name = Config.PINECONE_INDEX_NAME
    
    # Delete old index
    existing = [idx.name for idx in pc.list_indexes()]
    if index_name in existing:
        print(f"   Deleting old index (768-dim)")
        pc.delete_index(index_name)
        time.sleep(5)
    
    # Create new index with 384 dimensions
    print(f"   Creating new index (384-dim for HuggingFace)")
    pc.create_index(
        name=index_name,
        dimension=384,  # all-MiniLM-L6-v2 = 384 dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    
    time.sleep(5)
    print("✅ Index recreated!")
    print(f"   Dimension: 384 (smaller, faster)")
    print(f"   Using: HuggingFace Inference API (free)")

if __name__ == "__main__":
    recreate_index()
