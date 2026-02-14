import os
from pinecone import Pinecone, ServerlessSpec
from django.conf import settings


from .utils import get_book_embedding

# Create a Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

INDEX_NAME = "books-index"

# Create the index if it doesn't exist
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # match your embedding size
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # replace with your Pinecone env
        )
    )

# Connect to the index
index = pc.Index(INDEX_NAME)

def add_book_to_pinecone(book):
    text = f"{book.title} {book.description or ''}"
    emb = get_book_embedding(text)
    index.upsert(vectors=[(str(book.id), emb.tolist(), {"title": book.title, "author": book.author})])