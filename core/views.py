from rest_framework import generics, permissions
from .models import Book, Genre, UserBook
from .serializers import BookSerializer, GenreSerializer, UserBookSerializer

# -----------------------------
# Genre Views
# -----------------------------
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

# -----------------------------
# Book Views
# -----------------------------
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# -----------------------------
# UserBook Views
# -----------------------------
class UserBookListCreateView(generics.ListCreateAPIView):
    serializer_class = UserBookSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return UserBook.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        serializer.save(user_id=user_id)