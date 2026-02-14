# Standard library imports
# (none in your snippet, but keep here if needed)

# Django imports
from django.contrib.auth.models import User

# DRF imports
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

# Local app imports
from .models import Book, Genre, UserBook, Scan
from .serializers import (
    BookSerializer,
    GenreSerializer,
    UserBookSerializer,
    ScanSerializer,
    ScanDetectedBookSerializer,
)
from .tasks import process_scan
from .recommendations import recommend_books_for_user



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




# -----------------------------
# List & Create Scan
# -----------------------------

class ScanListCreateView(generics.ListCreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        scan = serializer.save(user_id=user_id)

        # Trigger async OCR
        process_scan.delay(scan.id)


# Recommendation API
# -----------------------------
class RecommendationView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        recommended_books = recommend_books_for_user(user, top_k=5)
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)