from ninja import NinjaAPI, Query
from typing import List, Optional

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from courses.models import Course, Enrollment, Lesson, Progress
from courses.schemas import CourseOut, CourseDetail

from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja_simple_jwt.auth.views.api import mobile_auth_router

from courses.permissions import is_admin, role_required
from courses.utils import get_real_user

from ninja.errors import HttpError

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
def list_courses(request, page: int = 1, page_size: int = 10, search: str = ""):
    qs = Course.objects.select_related("instructor", "category")

    if search:
        qs = qs.filter(title__icontains=search)

    start = (page - 1) * page_size
    end = start + page_size

    courses = qs[start:end]

    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor": c.instructor.username,
            "category": c.category.name if c.category else None
        }
        for c in courses
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
def create_course(request, title: str, description: str):
    user = get_real_user(request)

    course = Course.objects.create(
        title=title,
        description=description,
        instructor=user
    )

    return {"id": course.id, "title": course.title}


# owner only
@api.patch("/courses/{course_id}", auth=apiAuth)
def update_course(request, course_id: int, title: str = None):
    user = get_real_user(request)

    course = get_object_or_404(Course, id=course_id)

    if course.instructor != user:
        raise HttpError(403, "Not your course")

    if title:
        course.title = title
        course.save()

    return {"msg": "updated"}

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

    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course_id=course_id
    )

    return {"enrolled": True}


@api.get("/enrollments/my-courses", auth=apiAuth)
def my_courses(request):
    user = get_real_user(request)

    enrollments = Enrollment.objects.filter(user=user)

    return [
        {
            "course": e.course.title
        }
        for e in enrollments
    ]
