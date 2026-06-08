from django.contrib.auth.models import User
from courses.models import UserProfile
import time
from django.core.cache import cache
from ninja.errors import HttpError
from functools import wraps
import re
from django.core.exceptions import ValidationError

def get_real_user(request):
    return User.objects.get(id=request.user.id)

def get_user_role(user):
    return user.userprofile.role

# Rate Limiting
def rate_limit(max_requests=10, window=60):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Identifikasi pengguna berdasarkan IP Address
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            key = f"ratelimit_{func.__name__}_{ip}"
            
            # Ambil riwayat waktu request (dalam detik) dari Redis
            request_times = cache.get(key, [])
            now = time.time()
            
            # Hapus riwayat request yang terjadi lebih dari 60 detik yang lalu
            request_times = [t for t in request_times if now - t < window]
            
            # Blokir jika jumlah request sudah mencapai batas (60 kali)
            if len(request_times) >= max_requests:
                raise HttpError(429, "Too Many Requests. Please wait a minute.")
                
            # Catat waktu request yang baru
            request_times.append(now)
            
            # Simpan kembali ke Redis
            cache.set(key, request_times, timeout=window)
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


# Unit Testing

def is_valid_email(email):
    """Validator sederhana untuk email."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_pdf_size(file_size, max_mb=2):
    """Validator ukuran file (default maks 2MB)."""
    max_bytes = max_mb * 1024 * 1024
    if file_size > max_bytes:
        raise ValidationError(f"File size cannot exceed {max_mb}MB.")
    return True
