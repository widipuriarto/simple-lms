import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from courses.models import Course, Enrollment, Comment

@pytest.mark.django_db
def test_course_creation():
    # Test 1: Pembuatan model Course (Happy Path)
    instructor = User.objects.create(username="dosen1")
    course = Course.objects.create(
        title="Python Dasar",
        description="Belajar Python dari nol",
        instructor=instructor
    )
    assert course.title == "Python Dasar"
    assert course.instructor.username == "dosen1"
    # Memastikan representasi string __str__ bekerja dengan baik
    assert str(course) == "Python Dasar"

@pytest.mark.django_db
def test_enrollment_creation():
    # Test 2: Pembuatan model Enrollment (Happy Path)
    student = User.objects.create(username="siswa1")
    instructor = User.objects.create(username="dosen2")
    course = Course.objects.create(title="Django Dasar", instructor=instructor)
    
    enrollment = Enrollment.objects.create(user=student, course=course)
    assert enrollment.user.username == "siswa1"
    assert enrollment.course.title == "Django Dasar"
    # Memastikan format string Enrollment ("user - course")
    assert str(enrollment) == "siswa1 - Django Dasar"

@pytest.mark.django_db
def test_enrollment_unique_together():
    # Test 3: Siswa tidak bisa daftar course yang sama dua kali (Edge Case/Negative)
    student = User.objects.create(username="siswa2")
    instructor = User.objects.create(username="dosen3")
    course = Course.objects.create(title="React Dasar", instructor=instructor)
    
    # Pendaftaran pertama sukses
    Enrollment.objects.create(user=student, course=course)
    
    # Pendaftaran kedua harus ditolak oleh sistem database (memicu IntegrityError)
    with pytest.raises(IntegrityError):
        Enrollment.objects.create(user=student, course=course)

@pytest.mark.django_db
def test_comment_creation():
    # Test 4: Pembuatan model Comment (Happy Path)
    student = User.objects.create(username="siswa3")
    instructor = User.objects.create(username="dosen4")
    course = Course.objects.create(title="NextJS Dasar", instructor=instructor)
    
    comment = Comment.objects.create(
        user=student,
        course=course,
        content="Materi yang sangat bagus!"
    )
    assert comment.content == "Materi yang sangat bagus!"
    assert str(comment) == "Comment by siswa3 on NextJS Dasar"

@pytest.mark.django_db
def test_course_deletion_cascades_to_comments():
    # Test 5: Jika Course dihapus, Comment harus ikut terhapus (Edge Case / Cascade)
    student = User.objects.create(username="siswa4")
    instructor = User.objects.create(username="dosen5")
    course = Course.objects.create(title="Hapus Saya", instructor=instructor)
    
    Comment.objects.create(user=student, course=course, content="Komentar ini akan hilang")
    assert Comment.objects.count() == 1 # Memastikan data masuk
    
    # Menghapus course
    course.delete()
    
    # Memastikan komentar di dalamnya ikut hancur secara otomatis
    assert Comment.objects.count() == 0
