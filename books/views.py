from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics
from .models import Book, Review, Favorite
from .serializers import BookSerializer, ReviewSerializer

def index(request):
    """Главная страница приложения"""
    return render(request, 'index.html')

@ensure_csrf_cookie
def login(request):
    """Страница входа для пользователей"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                messages.error(request, 'Неверное имя пользователя или пароль')
                return render(request, 'login.html')
            
            auth_login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'login.html')

@ensure_csrf_cookie
def admin_login(request):
    """Страница входа для администраторов"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not (user.is_staff or user.is_superuser):
                messages.error(request, 'У вас нет прав администратора')
                return render(request, 'admin_login.html')
            
            auth_login(request, user)
            return redirect('admin:index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'admin_login.html')

@login_required
def user_dashboard(request):
    """Панель управления для обычных пользователей"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    books = Book.objects.all()
    return render(request, 'user_dashboard.html', {'books': books})

@login_required
@ensure_csrf_cookie
def book_detail(request, book_id):
    """Детальная страница книги"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    book = get_object_or_404(Book, id=book_id)
    
    # проверка рецензии
    user_review = None
    if request.user.username:
        user_review = Review.objects.filter(book=book, user=request.user.username).first()
    
    # проверка наличие книги
    is_favorite = False
    if request.user.username:
        is_favorite = Favorite.objects.filter(book=book, user_name=request.user.username).exists()
    
    return render(request, 'book_detail.html', {
        'book': book,
        'user_review': user_review,
        'is_favorite': is_favorite
    })

@login_required
def add_review(request, book_id):
    """Добавить рецензию к книге"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        # проверка рецензии пользователя
        existing_review = Review.objects.filter(book=book, user=request.user.username).first()
        if existing_review:
            messages.error(request, 'Вы уже писали рецензию на эту книгу')
            return redirect('book_detail', book_id=book_id)
        
        if not rating or not text:
            messages.error(request, 'Все поля должны быть заполнены')
            return redirect('book_detail', book_id=book_id)
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, 'Оценка должна быть от 1 до 5')
                return redirect('book_detail', book_id=book_id)
        except ValueError:
            messages.error(request, 'Неверная оценка')
            return redirect('book_detail', book_id=book_id)
        
        Review.objects.create(
            book=book,
            user=request.user.username,
            rating=rating,
            text=text
        )
        
        book.update_average_rating()
        
        messages.success(request, 'Рецензия успешно добавлена!')
        return redirect('book_detail', book_id=book_id)
    
    return redirect('book_detail', book_id=book_id)

@login_required
@ensure_csrf_cookie
def edit_review(request, review_id):
    """Редактировать рецензию"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user.username:
        messages.error(request, 'Вы можете редактировать только свои рецензии')
        return redirect('book_detail', book_id=review.book.id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        
        if not rating or not text:
            messages.error(request, 'Все поля должны быть заполнены')
            return render(request, 'edit_review.html', {'review': review})
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, 'Оценка должна быть от 1 до 5')
                return render(request, 'edit_review.html', {'review': review})
        except ValueError:
            messages.error(request, 'Неверная оценка')
            return render(request, 'edit_review.html', {'review': review})
        
        review.rating = rating
        review.text = text
        review.save()
        
        review.book.update_average_rating()
        
        messages.success(request, 'Рецензия успешно обновлена!')
        return redirect('book_detail', book_id=review.book.id)
    
    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review(request, review_id):
    """Удалить рецензию"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    review = get_object_or_404(Review, id=review_id)
    
    if review.user != request.user.username:
        messages.error(request, 'Вы можете удалять только свои рецензии')
        return redirect('book_detail', book_id=review.book.id)
    
    book_id = review.book.id
    book = review.book  
    review.delete()
    
    book.update_average_rating()
    
    messages.success(request, 'Рецензия успешно удалена!')
    return redirect('book_detail', book_id=book_id)

@login_required
@ensure_csrf_cookie
def add_book(request):
    """Добавить новую книгу"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        
        if not title or not author or not published_date:
            messages.error(request, 'Все поля должны быть заполнены')
            return render(request, 'add_book.html')
        
        try:
            Book.objects.create(
                title=title,
                author=author,
                published_date=published_date
            )
            messages.success(request, f'Книга "{title}" успешно добавлена!')
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении книги: {e}')
    
    return render(request, 'add_book.html')

@login_required
def add_to_favorites(request, book_id):
    """Добавить книгу в избранное"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    book = get_object_or_404(Book, id=book_id)
    
    if Favorite.objects.filter(book=book, user_name=request.user.username).exists():
        messages.error(request, 'Книга уже добавлена в избранное')
    else:
        Favorite.objects.create(
            book=book,
            user_name=request.user.username
        )
        messages.success(request, f'Книга "{book.title}" добавлена в избранное!')
    
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_favorites(request, book_id):
    """Удалить книгу из избранного"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    book = get_object_or_404(Book, id=book_id)
    favorite = Favorite.objects.filter(book=book, user_name=request.user.username).first()
    
    if favorite:
        favorite.delete()
        messages.success(request, f'Книга "{book.title}" удалена из избранного!')
    else:
        messages.error(request, 'Книга не найдена в избранном')
    
    return redirect('book_detail', book_id=book_id)

@login_required
def favorites_list(request):
    """Список избранных книг"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin:index')
    
    favorites = Favorite.objects.filter(user_name=request.user.username).select_related('book')
    books = [favorite.book for favorite in favorites]
    
    return render(request, 'favorites.html', {'books': books})

# API Views
class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        return queryset.order_by('-average_rating')


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs['book_id'])
        serializer.save(book=book)
        book.update_average_rating()
