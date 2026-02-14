from .models import Book, UserBook
from .utils import get_book_embedding, cosine_similarity
import numpy as np

def recommend_books_for_user(user, top_k=5):
    # Step 1: Get user's books
    user_books = UserBook.objects.filter(user=user)
    if not user_books.exists():
        return []

    # Step 2: Generate embeddings for user's books
    user_book_embeddings = []
    for ub in user_books:
        text = f"{ub.book.title} {ub.book.description or ''}"
        emb = get_book_embedding(text)
        user_book_embeddings.append(emb)

    # Step 3: Compute user profile embedding (average)
    user_embedding = np.mean(user_book_embeddings, axis=0)

    # Step 4: Get all books NOT in user's library
    user_book_ids = user_books.values_list("book_id", flat=True)
    candidate_books = Book.objects.exclude(id__in=user_book_ids)

    recommendations = []
    for book in candidate_books:
        text = f"{book.title} {book.description or ''}"
        emb = get_book_embedding(text)
        sim = cosine_similarity(user_embedding, emb)
        recommendations.append((book, sim))

    # Step 5: Sort by similarity
    recommendations.sort(key=lambda x: x[1], reverse=True)

    # Step 6: Return top K books
    top_books = [book for book, score in recommendations[:top_k]]
    return top_books