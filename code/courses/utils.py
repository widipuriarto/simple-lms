from django.contrib.auth.models import User
from courses.models import UserProfile

def get_real_user(request):
    return User.objects.get(id=request.user.id)

def get_user_role(user):
    return user.userprofile.role