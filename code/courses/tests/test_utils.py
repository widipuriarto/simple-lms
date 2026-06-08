import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from courses.utils import is_valid_email, validate_pdf_size, get_user_role

# Tanda ini memberitahu pytest bahwa test ini akan menyentuh database
@pytest.mark.django_db
def test_get_user_role_admin():
    # Test 1: Mengecek fungsi get_user_role untuk admin (Happy Path)
    user = User.objects.create(username="admin1")
    user.userprofile.role = "admin"
    user.userprofile.save()
    assert get_user_role(user) == "admin"

@pytest.mark.django_db
def test_get_user_role_student():
    # Test 2: Mengecek fungsi get_user_role untuk student (Default behavior)
    user = User.objects.create(username="student1")
    assert get_user_role(user) == "student"

def test_is_valid_email_success():
    # Test 3: Mengecek email yang benar (Happy Path)
    assert is_valid_email("mahasiswa@kampus.ac.id") is True

def test_is_valid_email_fail():
    # Test 4: Mengecek format email yang salah (Edge Case)
    assert is_valid_email("mahasiswa.kampus.ac.id") is False
    assert is_valid_email("mahasiswa@.com") is False

def test_validate_pdf_size():
    # Test 5: Mengecek validasi batas ukuran file PDF (Edge Case & Happy Path)
    # 1 MB = 1048576 bytes (Diharapkan LOLOS)
    assert validate_pdf_size(1048576) is True
    
    # 3 MB = 3145728 bytes (Diharapkan MUNCUL ERROR ValidationError)
    with pytest.raises(ValidationError):
        validate_pdf_size(3145728)
