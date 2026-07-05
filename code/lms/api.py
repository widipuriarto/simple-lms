from ninja import NinjaAPI, Query
from typing import List, Optional

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from courses.models import Course, Enrollment, Lesson, Progress, Comment
from courses.schemas import CourseOut, CourseDetail, CourseCreateSchema, CourseFilterSchema, CourseUpdateSchema, CommentOut, CommentCreateSchema, ReviewCreateSchema, ReviewOut, WishlistOut, StudentDashboardOut, AdminUserOut, AdminEnrollmentOut

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

from django.db.models import Q
from courses.models import Course, Enrollment, Lesson, Progress, Comment, Review, Wishlist

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
    cache_key = f"courses_{filters.search}_{filters.title}_{filters.category}_{filters.instructor}_{filters.level}_{filters.status}_{filters.ordering}"
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
    
    # FILTER SEARCH (Full-search title/description)
    if filters.search:
        # Mencari kursus jika judul ATAU deskripsi mengandung kata kunci
        qs = qs.filter(Q(title__icontains=filters.search) | Q(description__icontains=filters.search))

    # FILTER LEVEL
    if filters.level:
        qs = qs.filter(level__iexact=filters.level)

    # FILTER STATUS
    if filters.status:
        qs = qs.filter(status__iexact=filters.status)


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

@api.post("/courses/{course_id}/reviews", response={201: dict, 400: dict, 404: dict}, auth=apiAuth)
@role_required(["student", "instructor", "admin"])
def create_review(request, course_id: int, payload: ReviewCreateSchema):
    user = get_real_user(request)
    course = get_object_or_404(Course, id=course_id)
    
    # Cek apakah user sudah pernah memberi review di course ini
    if Review.objects.filter(user=user, course=course).exists():
        return 400, {"message": "You have already reviewed this course"}
    
    # Aturan: Student hanya boleh review kalau sudah Enroll
    if user.userprofile.role == "student" and not Enrollment.objects.filter(user=user, course=course).exists():
        return 400, {"message": "You must be enrolled to review this course"}

    Review.objects.create(
        user=user,
        course=course,
        rating=payload.rating,
        comment=payload.comment
    )
    return 201, {"message": "Review submitted successfully"}

@api.get("/courses/{course_id}/reviews", response=List[ReviewOut])
@paginate
def list_reviews(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    return Review.objects.filter(course=course).order_by('-created_at')

@api.post("/wishlist/{course_id}", response={200: dict, 404: dict}, auth=apiAuth)
@role_required(["student"])
def toggle_wishlist(request, course_id: int):
    user = get_real_user(request)
    course = get_object_or_404(Course, id=course_id)
    
    # Jika sudah ada, hapus. Jika belum, tambahkan.
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, course=course)
    
    if not created:
        wishlist_item.delete()
        return 200, {"message": "Course removed from wishlist"}
        
    return 200, {"message": "Course added to wishlist"}

@api.get("/wishlist", response=List[WishlistOut], auth=apiAuth)
@role_required(["student"])
@paginate
def list_wishlist(request):
    user = get_real_user(request)
    # Gunakan select_related untuk menghemat query database (optimasi)
    return Wishlist.objects.filter(user=user).select_related('course').order_by('-created_at')


@api.get("/courses/{course_id}", response=CourseDetail)
@rate_limit(max_requests=60, window=60)
def course_detail(request, course_id: int):
    # Menggunakan prefetch_related pada 'sections__lessons' untuk optimasi query berlapis
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category').prefetch_related('sections__lessons'), 
        id=course_id
    )
    
    # Format manual struktur JSON agar sesuai dengan schema hirarki yang baru
    data = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor.username,
        "category": course.category.name if course.category else None,
        "level": course.level,
        "status": course.status,
        "sections": [
            {
                "id": section.id,
                "title": section.title,
                "order": section.order,
                "lessons": [
                    {"id": lesson.id, "title": lesson.title, "order": lesson.order}
                    for lesson in section.lessons.all()
                ]
            }
            for section in course.sections.all()
        ]
    }
    
    return data

@api.get("/courses/{course_id}/progress", response={200: dict, 404: dict}, auth=apiAuth)
@role_required(["student"])
def course_progress(request, course_id: int):
    user = get_real_user(request)
    course = get_object_or_404(Course, id=course_id)
    
    # Proteksi: Hanya siswa yang terdaftar yang bisa melihat progres belajarnya
    if not Enrollment.objects.filter(user=user, course=course).exists():
        return 404, {"message": "You are not enrolled in this course"}
        
    total_lessons = Lesson.objects.filter(course=course).count()
    
    # Mencegah error pembagian dengan nol (ZeroDivisionError)
    if total_lessons == 0:
        return 200, {"progress_percentage": 0.0, "completed_lessons": 0, "total_lessons": 0}
        
    completed_lessons = Progress.objects.filter(
        user=user, 
        lesson__course=course, 
        completed=True
    ).count()
    
    # Rumus persentase penyelesaian
    percentage = (completed_lessons / total_lessons) * 100
    
    return 200, {
        "progress_percentage": round(percentage, 2),
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons
    }

@api.get("/dashboard/student", response=StudentDashboardOut, auth=apiAuth)
@role_required(["student"])
def student_dashboard(request):
    user = get_real_user(request)
    
    # Ambil semua pendaftaran (enrollment) yang dimiliki siswa
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__instructor').prefetch_related('course__lessons')
    
    active_courses = []
    completed_courses = []
    enrolled_course_ids = []
    enrolled_categories = set()
    
    for enrollment in enrollments:
        course = enrollment.course
        enrolled_course_ids.append(course.id)
        
        # Simpan kategori kursus untuk algoritma rekomendasi di bawah nanti
        if course.category_id:
            enrolled_categories.add(course.category_id)
            
        total_lessons = course.lessons.count()
        if total_lessons == 0:
            percentage = 0.0
        else:
            completed_lessons = Progress.objects.filter(
                user=user, 
                lesson__course=course, 
                completed=True
            ).count()
            percentage = (completed_lessons / total_lessons) * 100
            
        course_data = {
            "id": course.id,
            "title": course.title,
            "instructor": course.instructor.username,
            "progress_percentage": round(percentage, 2)
        }
        
        if percentage >= 100.0:
            completed_courses.append(course_data)
        else:
            active_courses.append(course_data)
            
    # Logika Rekomendasi: Cari kursus di kategori yang diminati, berstatus published, yang BELUM didaftar
    recommended_courses = Course.objects.filter(
        category_id__in=enrolled_categories,
        status='published'
    ).exclude(
        id__in=enrolled_course_ids
    ).select_related('instructor', 'category')[:5] # Batasi 5 rekomendasi
    
    return {
        "active_courses": active_courses,
        "completed_courses": completed_courses,
        "recommended_courses": recommended_courses
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

    # Hapus cache setiap ada perubahan data
    cache.clear()

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
    
    # Hapus cache
    cache.clear()

    return {"status": "success", "message": "Course updated"}

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

@api.get("/admin/users", response=List[AdminUserOut], auth=apiAuth)
@role_required("admin")
def list_users(request):
    return User.objects.select_related("userprofile").all()

@api.get("/admin/enrollments", response=List[AdminEnrollmentOut], auth=apiAuth)
@role_required("admin")
def list_enrollments(request):
    return Enrollment.objects.select_related("user", "course").all()

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

@api.get("/courses/{course_id}/comments", response=List[CommentOut])
def list_comments(request, course_id: int):
    course = get_object_or_404(Course, id=course_id)
    comments = Comment.objects.filter(course=course).select_related('user').order_by('-created_at')
    
    return [
        {
            "id": c.id,
            "user": c.user.username,
            "content": c.content,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for c in comments
    ]

@api.post("/courses/{course_id}/comments", auth=apiAuth)
def create_comment(request, course_id: int, payload: CommentCreateSchema):
    user = get_real_user(request)
    course = get_object_or_404(Course, id=course_id)
    
    comment = Comment.objects.create(
        user=user,
        course=course,
        content=payload.content
    )
    return {"message": "Comment created", "id": comment.id}

@api.delete("/comments/{comment_id}", auth=apiAuth)
def delete_comment(request, comment_id: int):
    user = get_real_user(request)
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Hanya admin atau pembuat komentar yang bisa menghapusnya
    if user.userprofile.role != "admin" and comment.user != user:
        from ninja.errors import HttpError
        raise HttpError(403, "Not allowed to delete this comment")
        
    comment.delete()
    return {"message": "Comment deleted"}

