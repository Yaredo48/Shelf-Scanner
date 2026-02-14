from django.contrib import admin
from .models import Book, Genre, BookGenres, UserBook, Scan, ScanDetectedBook

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookGenres)
admin.site.register(UserBook)
admin.site.register(Scan)
admin.site.register(ScanDetectedBook)