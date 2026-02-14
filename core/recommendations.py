from .models import Book, UserBook
from .utils import get_book_embedding, cosine_similarity
import numpy as np
from .pinecone_utils import index
from django.db.models import Q



def recommend_books_for_user(user, top_k=5):
    # 1. Get user books
    user_books = UserBook.objects.filter(user=user)
    if not user_books.exists():
        return []

    # 2. Generate user embedding (average of their books)
    embeddings = []
    for ub in user_books:
        text = f"{ub.book.title} {ub.book.description or ''}"
        emb = get_book_embedding(text)
        embeddings.append(emb)
    user_embedding = embeddings[0] if len(embeddings) == 1 else np.mean(embeddings, axis=0)

    # 3. Query Pinecone
    results = index.query(
        vector=user_embedding.tolist(),
        top_k=top_k + user_books.count(),  # +exclude user's books
        include_metadata=True
    )

    # 4. Filter out books user already has
    user_book_ids = set(str(b.book.id) for b in user_books)
    recommendations = []
    for match in results["matches"]:
        if match["id"] not in user_book_ids:
            book = Book.objects.get(id=int(match["id"]))
            recommendations.append(book)
            if len(recommendations) == top_k:
                break

    return recommendations


