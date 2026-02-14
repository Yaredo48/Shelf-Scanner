from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Genre Model
# -----------------------------
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -----------------------------
# Book Model
# -----------------------------
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True)
    published_year = models.IntegerField(blank=True, null=True)
    cover_url = models.URLField(blank=True)
    metadata_source = models.CharField(max_length=50, blank=True)

    genres = models.ManyToManyField(Genre, through="BookGenres", related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author}"


# -----------------------------
# Junction Table: BookGenres
# -----------------------------
class BookGenres(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("book", "genre")

    def __str__(self):
        return f"{self.book.title} - {self.genre.name}"


# -----------------------------
# UserBooks Model (User Library)
# -----------------------------
class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, choices=[("scan", "Scan"), ("manual", "Manual")], default="manual")
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.username} owns {self.book.title}"


# -----------------------------
# Scan Model (User uploads shelf image)
# -----------------------------
class Scan(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scans")
    image = models.ImageField(upload_to="scans/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Scan {self.id} by {self.user.username}"


# -----------------------------
# ScanDetectedBook Model
# -----------------------------
class ScanDetectedBook(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, related_name="detected_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    confidence_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.book.title} detected in Scan {self.scan.id}"