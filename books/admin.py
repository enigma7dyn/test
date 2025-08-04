from django.contrib import admin
from .models import Book, Review, Favorite

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'average_rating')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'author')
    ordering = ('-average_rating',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user', 'text')
    ordering = ('-created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('book', 'user_name', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user_name', 'book__title')
    ordering = ('-added_at',)
