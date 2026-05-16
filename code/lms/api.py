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
@paginate
def list_courses(request, filters: CourseFilterSchema = Query(...)):
    
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

    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor.username,
            "category": c.category.name if c.category else None
        }
        for c in qs
    ]

@api.get("/courses/{course_id}", response=CourseDetail)
def course_detail(request, course_id: int):
    c = get_object_or_404(
        Course.objects.select_related("instructor", "category").prefetch_related("lessons"),
        id=course_id
    )

    return {
        "id": c.id,
        "title": c.title,
        "description": c.description,
        "instructor": c.instructor.username,
        "category": c.category.name if c.category else None,
        "lessons": [l.title for l in c.lessons.all()]
    }


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

    return {
        "msg": "updated",
        "updated_fields": list(update_data.keys())
    }

# admin only
@api.delete("/courses/{course_id}", auth=apiAuth)
@role_required("admin")
def delete_course(request, course_id: int):
    Course.objects.filter(id=course_id).delete()
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