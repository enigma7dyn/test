from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Создает суперпользователя admin с паролем admin123'

    def handle(self, *args, **options):
        try:
            # Удаляем существующего пользователя admin если есть
            User.objects.filter(username='admin').delete()
            
            # Создаем нового суперпользователя
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Суперпользователь успешно создан!')
            )
            self.stdout.write('👤 Логин: admin')
            self.stdout.write('🔑 Пароль: admin123')
            self.stdout.write('🌐 Админка: http://127.0.0.1:8000/admin/')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка: {e}')
            ) 