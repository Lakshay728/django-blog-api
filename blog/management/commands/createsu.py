from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=os.environ.get('ADMIN_USERNAME', 'admin'),
                password=os.environ.get('ADMIN_PASSWORD', 'admin123'),
                email=os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            )
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Superuser already exists.')
