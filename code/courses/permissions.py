from ninja.errors import HttpError
from django.contrib.auth.models import User
import functools

def get_real_user(request):
    return User.objects.get(id=request.user.id)

def is_admin(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        user = get_real_user(request)

        if user.userprofile.role != "admin":
            return {"detail": "Forbidden"}

        return func(request, *args, **kwargs)
    return wrapper

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]
        
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            user = get_real_user(request)
            if user.userprofile.role not in roles:
                raise HttpError(403, f"Forbidden: Requires {roles} role")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator