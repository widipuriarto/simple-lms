from django.http import JsonResponse
from .models import Course, Enrollment
from django.db.models import Count

def course_list(request):
    data = []

    courses = Course.objects.select_related(
        'instructor', 'category'
    ).prefetch_related(
        'lessons'
    )

    for c in courses:
        lessons = []
        for l in c.lessons.all():
            lessons.append({
                "title": l.title
            })

        data.append({
            "title": c.title,
            "instructor": c.instructor.username,
            "category": c.category.name if c.category else None,
            "lessons": lessons
        })

    return JsonResponse(data, safe=False)

def student_dashboard(request):
    data = []

    enrollments = Enrollment.objects.select_related(
        'course', 'user'
    ).annotate(
        total_lessons=Count('course__lessons')
    )

    for e in enrollments:
        data.append({
            "user": e.user.username,
            "course": e.course.title,
            "total_lessons": e.total_lessons
        })

    return JsonResponse(data, safe=False)