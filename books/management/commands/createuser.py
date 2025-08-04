from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Создает обычного пользователя user с паролем user123'

    def handle(self, *args, **options):
        try:
            # Удаляем существующего пользователя user если есть
            User.objects.filter(username='user').delete()
            
            # Создаем нового обычного пользователя
            user = User.objects.create_user(
                username='user',
                email='user@example.com',
                password='user123',
                is_staff=False,
                is_superuser=False
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Обычный пользователь успешно создан!')
            )
            self.stdout.write('👤 Логин: user')
            self.stdout.write('🔑 Пароль: user123')
            self.stdout.write('🌐 Вход: http://127.0.0.1:8000/login/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка: {e}')
            ) 