import os
from celery import Celery

# 1. Beritahu Celery di mana letak pengaturan (settings) Django kita
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

# 2. Buat aplikasi Celery dengan nama 'lms'
app = Celery('lms')

# 3. Minta Celery untuk membaca konfigurasinya dari settings.py Django
# Parameter namespace='CELERY' berarti Celery hanya akan membaca variabel 
# yang diawali dengan "CELERY_" (yang sudah kita buat di Tahap 1)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Celery akan otomatis mencari file bernama 'tasks.py' di setiap folder aplikasi (seperti 'courses')
app.autodiscover_tasks()

# Task bawaan untuk memastikan Celery berjalan
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
