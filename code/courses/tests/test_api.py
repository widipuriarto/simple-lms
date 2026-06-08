import pytest
import json
from django.contrib.auth.models import User
from courses.models import Course, Enrollment, Comment

# ==========================================
# FIXTURES (Persiapan Sistem sebelum testing)
# ==========================================
@pytest.fixture
def api_client():
    from django.test import Client
    return Client()

@pytest.fixture
def admin_user():
    user = User.objects.create_user(username="admin_test", password="password123", email="admin@test.com")
    user.userprofile.role = "admin"
    user.userprofile.save()
    return user

@pytest.fixture
def instructor_user():
    user = User.objects.create_user(username="inst_test", password="password123", email="inst@test.com")
    user.userprofile.role = "instructor"
    user.userprofile.save()
    return user

@pytest.fixture
def student_user():
    return User.objects.create_user(username="student_test", password="password123", email="student@test.com")

def get_auth_headers(client, username, password="password123"):
    """Fungsi pembantu untuk simulasi LOGIN dan mendapatkan Token JWT."""
    payload = {"username": username, "password": password}
    
    # PERBAIKAN: Menggunakan data=json.dumps() alih-alih json=
    response = client.post("/api/v1/auth/sign-in", data=json.dumps(payload), content_type="application/json")
    
    if response.status_code == 200:
        token = response.json().get("access")
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    return {}

# ==========================================
# PENGUJIAN COURSE CRUD & SKENARIO NEGATIF
# ==========================================
@pytest.mark.django_db
def test_course_crud_and_negative(api_client, admin_user, instructor_user, student_user):
    headers_admin = get_auth_headers(api_client, admin_user.username)
    headers_inst = get_auth_headers(api_client, instructor_user.username)
    headers_student = get_auth_headers(api_client, student_user.username)
    
    # --- PENGUJIAN NEGATIF 1: Mengakses API tanpa token (Unauthorized) ---
    payload = {"title": "Test Course", "description": "Deskripsi Test"}
    res_no_auth = api_client.post("/api/v1/protected/courses", data=json.dumps(payload), content_type="application/json")
    assert res_no_auth.status_code == 401 
    
    # --- PENGUJIAN NEGATIF 2: Mengakses API dengan role yang salah (Forbidden) ---
    res_student_auth = api_client.post("/api/v1/protected/courses", data=json.dumps(payload), content_type="application/json", **headers_student)
    assert res_student_auth.status_code == 403 
    
    # --- INTEGRASI: CREATE Course (POST - Skenario Sukses) ---
    # Harus instructor
    response = api_client.post("/api/v1/protected/courses", data=json.dumps(payload), content_type="application/json", **headers_inst)
    assert response.status_code == 200
    course_id = response.json().get("id")
    
    # --- INTEGRASI: READ Course (GET) ---
    response = api_client.get(f"/api/v1/protected/courses/{course_id}", **headers_inst)
    assert response.status_code == 200
    assert response.json().get("title") == "Test Course"
    
    # --- INTEGRASI: UPDATE Course (PATCH) ---
    # Hanya instructor pemilik yang bisa edit
    update_payload = {"title": "Updated Course"}
    response = api_client.patch(f"/api/v1/protected/courses/{course_id}", data=json.dumps(update_payload), content_type="application/json", **headers_inst)
    assert response.status_code == 200
    assert response.json().get("msg") == "updated"
    
    # --- PENGUJIAN NEGATIF 3: Student mencoba menghapus course (Forbidden) ---
    res_delete_fail = api_client.delete(f"/api/v1/protected/courses/{course_id}", **headers_student)
    assert res_delete_fail.status_code == 403
    
    # --- INTEGRASI: DELETE Course (DELETE - Skenario Sukses) ---
    # Harus admin
    response = api_client.delete(f"/api/v1/protected/courses/{course_id}", **headers_admin)
    assert response.status_code == 200

# ==========================================
# PENGUJIAN ENROLLMENT API
# ==========================================
@pytest.mark.django_db
def test_enrollment_api(api_client, instructor_user, student_user):
    headers_inst = get_auth_headers(api_client, instructor_user.username)
    headers_student = get_auth_headers(api_client, student_user.username)
    
    # Persiapan: Instructor membuat course terlebih dahulu
    payload = {"title": "Kursus", "description": "A"}
    res = api_client.post("/api/v1/protected/courses", data=json.dumps(payload), content_type="application/json", **headers_inst)
    course_id = res.json().get("id")
    
    # INTEGRASI: POST Enroll
    res_enroll = api_client.post(f"/api/v1/protected/enrollments?course_id={course_id}", **headers_student)
    assert res_enroll.status_code == 200
    
    # INTEGRASI: GET Members (Melihat daftarnya)
    res_my_courses = api_client.get("/api/v1/protected/enrollments/my-courses", **headers_student)
    assert res_my_courses.status_code == 200
    assert len(res_my_courses.json()) == 1

# ==========================================
# PENGUJIAN COMMENT API
# ==========================================
@pytest.mark.django_db
def test_comment_api(api_client, instructor_user, student_user):
    headers_inst = get_auth_headers(api_client, instructor_user.username)
    headers_student = get_auth_headers(api_client, student_user.username)
    
    # Persiapan: Instructor membuat course
    payload = {"title": "Komen Course", "description": "A"}
    res = api_client.post("/api/v1/protected/courses", data=json.dumps(payload), content_type="application/json", **headers_inst)
    course_id = res.json().get("id")
    
    # INTEGRASI: POST Comment (Sebagai student)
    comment_payload = {"content": "Halo Dunia"}
    res_post = api_client.post(f"/api/v1/protected/courses/{course_id}/comments", data=json.dumps(comment_payload), content_type="application/json", **headers_student)
    assert res_post.status_code == 200
    comment_id = res_post.json().get("id")
    
    # INTEGRASI: GET Comments
    res_get = api_client.get(f"/api/v1/protected/courses/{course_id}/comments", **headers_student)
    assert res_get.status_code == 200
    
    # INTEGRASI: DELETE Comment (Student menghapus komentarnya sendiri)
    res_del = api_client.delete(f"/api/v1/protected/comments/{comment_id}", **headers_student)
    assert res_del.status_code == 200
