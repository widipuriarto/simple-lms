# Pastikan aplikasi Celery selalu di-import saat Django menyala
from .celery import app as celery_app

# Mengekspos variabel agar bisa dikenali oleh sistem
__all__ = ('celery_app',)
