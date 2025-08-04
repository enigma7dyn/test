from django.urls import path
from .views import BookListCreateView, ReviewListCreateView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:book_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]


