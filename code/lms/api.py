from ninja import NinjaAPI, Query
from typing import List, Optional

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from courses.models import Course, Enrollment, Lesson, Progress
from courses.schemas import CourseOut, CourseDetail, CourseCreateSchema, CourseFilterSchema, CourseUpdateSchema

from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja_simple_jwt.auth.views.api import mobile_auth_router

from courses.permissions import is_admin, role_required
from courses.utils import get_real_user

from ninja.errors import HttpError

from ninja.pagination import paginate

from ninja.files import UploadedFile
from ninja import File
from django.core.files.storage import default_storage
from django.core.cache import cache

from courses.utils import rate_limit
from courses.mongodb import log_activity
from courses.mongodb import log_activity, get_activity_report
from courses.tasks import send_enrollment_email, generate_certificate, export_course_report

# PUBLIC API
apiv1 = NinjaAPI(
    title="Public API",
    version="1.0.0",
    urls_namespace="api-public"
)

apiv1.add_router("/auth/", mobile_auth_router)

# AUTH handler
apiAuth = HttpJwtAuth()

# PROTECTED API
api = NinjaAPI(
    title="Protected API",
    version="1.0.0",
    urls_namespace="api-protected"
)


@api.get("/auth/me", auth=apiAuth)
def get_current_user(request):
    user = get_real_user(request)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.userprofile.role,
    }

@api.get("/")
def root(request):
    return {"message": "API is working 🚀"}

@api.get("/courses", response=List[CourseOut])
@rate_limit(max_requests=60, window=60) 
@paginate
def list_courses(request, filters: CourseFilterSchema = Query(...)):
    
    # --- REDIS CACHING START ---
    cache_key = f"courses_{filters.title}_{filters.category}_{filters.instructor}_{filters.ordering}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    # --- REDIS CACHING END ---

    qs = Course.objects.select_related(
        "instructor",
        "category"
    )

    # FILTER TITLE
    if filters.title:
        qs = qs.filter(title__icontains=filters.title)

    # FILTER CATEGORY
    if filters.category:
        qs = qs.filter(category_id=filters.category)

    # FILTER INSTRUCTOR
    if filters.instructor:
        qs = qs.filter(
            instructor__username__icontains=filters.instructor
        )

    # SORTING WHITELIST
    allowed_order_fields = [
        "title",
        "-title",
        "created_at",
        "-created_at",
    ]

    if filters.ordering in allowed_order_fields:
        qs = qs.order_by(filters.ordering)

    data = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor.username,
            "category": c.category.name if c.category else None
        }
        for c in qs
    ]
    
    # --- SIMPAN KE CACHE (15 Menit) ---
    cache.set(cache_key, data, timeout=60*15)
    
    return data

@api.get("/courses/{course_id}", response=CourseDetail)
@rate_limit(max_requests=60, window=60)
def course_detail(request, course_id: int):
    # --- REDIS CACHING START ---
    cache_key = f"course_detail_{course_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    # --- REDIS CACHING END ---

    c = get_object_or_404(
        Course.objects.select_related("instructor", "category").prefetch_related("lessons"),
        id=course_id
    )

    data = {
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "instructor": c.instructor.username,
        "category": c.category.name if c.category else None,
        "lessons": [l.title for l in c.lessons.all()]
    }
    
    # --- SIMPAN KE CACHE (15 Menit) ---
    cache.set(cache_key, data, timeout=60*15)
    
    return data


@api.post("/enrollments/{enrollment_id}/progress", auth=apiAuth)
def mark_progress(request, enrollment_id: int, lesson_id: int):
    user = get_real_user(request)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, _ = Progress.objects.get_or_create(
        user=user,
        lesson=lesson
    )
    progress.completed = True
    progress.save()

    # --- MONGODB LOGGING START ---
    log_activity(
        user_id=user.id,
        action="COMPLETE_LESSON",
        details={"lesson_id": lesson.id, "lesson_title": lesson.title}
    )
    # --- MONGODB LOGGING END ---

    generate_certificate.delay(user.username, lesson.course.title)

    return {"status": "completed"}


# Instructor endpoint to create a course

@api.post("/courses", auth=apiAuth)
@role_required("instructor")
def create_course(request, payload: CourseCreateSchema):
    user = get_real_user(request)

    course = Course.objects.create(
        title=payload.title,
        description=payload.description,
        instructor=user
    )

    return {
        "id": course.id,
        "title": course.title
    }


# owner only
@api.patch("/courses/{course_id}", auth=apiAuth)
def update_course(
    request,
    course_id: int,
    payload: CourseUpdateSchema
):
    user = get_real_user(request)

    course = get_object_or_404(Course, id=course_id)

    # owner validation
    if course.instructor != user:
        raise HttpError(403, "Not your course")

    # only update sent fields
    update_data = payload.dict(exclude_unset=True)

    for attr, value in update_data.items():
        setattr(course, attr, value)

    course.save()

    # --- CACHE INVALIDATION ---
    cache.delete(f"course_detail_{course_id}") # Hapus cache spesifik untuk course ini
    cache.clear() # Hapus seluruh cache (termasuk list course) karena datanya berubah

    return {
        "msg": "updated",
        "updated_fields": list(update_data.keys())
    }

# admin only
@api.delete("/courses/{course_id}", auth=apiAuth)
@role_required("admin")
def delete_course(request, course_id: int):
    Course.objects.filter(id=course_id).delete()
    
    # --- CACHE INVALIDATION ---
    cache.delete(f"course_detail_{course_id}")
    cache.clear()

    return {"msg": "deleted"}

# student only
@api.post("/enrollments", auth=apiAuth)
@role_required("student")
def enroll_course(request, course_id: int):
    user = get_real_user(request)

    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course=course
    )

    # --- MONGODB LOGGING START ---
    log_activity(
        user_id=user.id,
        action="ENROLL_COURSE",
        details={"course_id": course.id, "course_title": course.title}
    )
    # --- MONGODB LOGGING END ---

    # --- PANGGIL CELERY TASK ---
    # .delay() melempar tugas ini ke latar belakang!
    send_enrollment_email.delay(user.email, course.title)

    return {
        "enrolled": True,
        "course": course.title
    }


@api.get("/enrollments/my-courses", auth=apiAuth)
def my_courses(request):
    user = get_real_user(request)

    enrollments = Enrollment.objects.select_related(
        "course"
    ).filter(user=user)

    return [
        {
            "course": e.course.title
        }
        for e in enrollments
    ]


@api.post("/upload", auth=apiAuth)
def upload_file(
    request,
    file: UploadedFile = File(...)
):
    # VALID EXTENSIONS
    allowed_types = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]

    # VALIDATE TYPE
    if file.content_type not in allowed_types:
        raise HttpError(
            400,
            "Only JPG, PNG, and PDF allowed"
        )

    # VALIDATE SIZE (2MB)
    max_size = 2 * 1024 * 1024

    if file.size > max_size:
        raise HttpError(
            400,
            "File too large (max 2MB)"
        )

    # SAVE FILE
    file_name = default_storage.save(
        f"uploads/{file.name}",
        file
    )

    return {
        "message": "Upload successful",
        "file": file_name,
        "url": f"/media/{file_name}"
    }

@api.get("/analytics/reports", auth=apiAuth)
@role_required("admin")
def get_analytics(request):
    """
    Endpoint khusus admin untuk melihat statistik aktivitas platform.
    """
    report = get_activity_report()
    return {
        "status": "success",
        "data": report
    }

@api.post("/analytics/export", auth=apiAuth)
@role_required("admin")
def trigger_export(request):
    """
    Endpoint admin untuk memicu pembuatan laporan CSV raksasa di latar belakang.
    """
    user = get_real_user(request)
    
    # --- PANGGIL CELERY TASK ---
    export_course_report.delay(user.email)
    
    return {
        "message": "Proses ekspor dimulai! Anda akan menerima laporannya via email beberapa saat lagi."
    }

