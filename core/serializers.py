from rest_framework import serializers
from .models import Book, Genre, UserBook, Scan, ScanDetectedBook
from django.contrib.auth.models import User

from .models import Scan, ScanDetectedBook

# -----------------------------
# Genre Serializer
# -----------------------------
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


# -----------------------------
# Book Serializer
# -----------------------------
class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "description", "published_year", "cover_url", "metadata_source", "genres"]


# -----------------------------
# UserBook Serializer
# -----------------------------
class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source="book", write_only=True)

    class Meta:
        model = UserBook
        fields = ["id", "user", "book", "book_id", "added_at", "source", "rating"]


# -----------------------------
# User Serializer (basic)
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]





# -----------------------------
# Scan Serializer
# -----------------------------
class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ["id", "user", "image", "status", "created_at", "processed_at"]
        read_only_fields = ["status", "created_at", "processed_at"]

# -----------------------------
# Scan Detected Book Serializer
# -----------------------------
class ScanDetectedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = ScanDetectedBook
        fields = ["id", "scan", "book", "confidence_score"]