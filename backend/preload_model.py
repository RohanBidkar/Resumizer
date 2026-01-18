from sentence_transformers import SentenceTransformer
import os

print("Downloading embedding model...")
# This will download and cache the model in the default torch cache directory
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("Model downloaded successfully!")
