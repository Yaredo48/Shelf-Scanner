from django.urls import path
from .views import GenreListCreateView, BookListCreateView, UserBookListCreateView

#from .views.recommendations import RecommendationView
from .views import RecommendationView

urlpatterns = [
    # Genres
    path("genres/", GenreListCreateView.as_view(), name="genre-list-create"),

    # Books
    path("books/", BookListCreateView.as_view(), name="book-list-create"),

    # User Library
    path("users/<int:user_id>/books/", UserBookListCreateView.as_view(), name="userbook-list-create"),
    path("users/<int:user_id>/scans/", BookListCreateView.as_view(), name="user-scan-list-create"),
    path("users/<int:user_id>/recommendations/", RecommendationView.as_view(), name="user-recommendations"),

]