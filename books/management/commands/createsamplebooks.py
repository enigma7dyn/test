from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date

class Command(BaseCommand):
    help = 'Создает тестовые книги для демонстрации'

    def handle(self, *args, **options):
        try:
            # Удаляем существующие книги
            Book.objects.all().delete()
            
            # Создаем тестовые книги
            books_data = [
                {
                    'title': 'Война и мир',
                    'author': 'Лев Толстой',
                    'published_date': date(1869, 1, 1),
                    'average_rating': 4.8
                },
                {
                    'title': 'Преступление и наказание',
                    'author': 'Федор Достоевский',
                    'published_date': date(1866, 1, 1),
                    'average_rating': 4.7
                },
                {
                    'title': 'Мастер и Маргарита',
                    'author': 'Михаил Булгаков',
                    'published_date': date(1967, 1, 1),
                    'average_rating': 4.9
                },
                {
                    'title': 'Евгений Онегин',
                    'author': 'Александр Пушкин',
                    'published_date': date(1833, 1, 1),
                    'average_rating': 4.6
                },
                {
                    'title': 'Герой нашего времени',
                    'author': 'Михаил Лермонтов',
                    'published_date': date(1840, 1, 1),
                    'average_rating': 4.5
                }
            ]
            
            for book_data in books_data:
                Book.objects.create(**book_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Создано {len(books_data)} тестовых книг!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка: {e}')
            ) 