from .models import Book
from .utils import get_book_embedding
from .pinecone_utils import index

def upload_all_books_to_pinecone():
    books = Book.objects.all()
    vectors = []

    for book in books:
        text = f"{book.title} {book.description or ''}"
        emb = get_book_embedding(text)
        vectors.append((str(book.id), emb.tolist(), {"title": book.title, "author": book.author}))

    # Batch upsert
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i + batch_size])