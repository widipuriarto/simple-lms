from django.db import models
from django.contrib.auth.models import User

class CourseQuerySet(models.QuerySet):
    def for_listing(self):
        return self.select_related('instructor', 'category')

class EnrollmentQuerySet(models.QuerySet):
    def for_student_dashboard(self):
        return self.select_related('course').prefetch_related('course__lessons')



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=['title'], name='idx_course_title'),
        ]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    order = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['course', 'order'], name='idx_lesson_course_order'),
        ]

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    objects = EnrollmentQuerySet.as_manager()

    class Meta:
        unique_together = ('user', 'course')
        indexes = [
            models.Index(fields=['user', 'course'], name='idx_enrollment_user_course'),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class Progress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

