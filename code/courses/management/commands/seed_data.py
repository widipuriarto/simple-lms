from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Lesson, Enrollment, Progress, UserProfile
import random


class Command(BaseCommand):
    help = "Reset & Seed data (20 students)"

    def handle(self, *args, **kwargs):

        print("🧹 Deleting old data...")

        # URUTAN PENTING (hindari FK error)
        Progress.objects.all().delete()
        Enrollment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        print("✅ Old data cleared")

        # ------------------------
        # USERS (ALL STUDENT)
        # ------------------------
        print("Creating 20 student users...")

        users = []

        for i in range(20):
            user = User.objects.create_user(
                username=f"student{i}",
                password="password"
            )

            # set role = student
            profile = user.userprofile
            profile.role = "student"
            profile.save()

            users.append(user)

        print("✅ 20 students created")

        # ------------------------
        # CATEGORY
        # ------------------------
        print("Creating categories...")

        categories = []
        for i in range(3):
            cat = Category.objects.create(name=f"Category {i}")
            categories.append(cat)

        # ------------------------
        # COURSES
        # ------------------------
        print("Creating courses...")

        courses = []

        # ⚠️ karena semua student → kita pilih 1 user jadi instructor dummy
        instructor = users[0]

        for i in range(10):
            course = Course.objects.create(
                title=f"Course {i}",
                description="Lorem ipsum dolor sit amet",
                instructor=instructor,
                category=random.choice(categories)
            )
            courses.append(course)

        # ------------------------
        # LESSONS
        # ------------------------
        print("Creating lessons...")

        for course in courses:
            for i in range(3):
                Lesson.objects.create(
                    title=f"{course.title} - Lesson {i}",
                    content="Lesson content",
                    course=course,
                    order=i
                )

        # ------------------------
        # ENROLLMENTS
        # ------------------------
        print("Creating enrollments...")

        enrollments = []

        for user in users:
            for course in random.sample(courses, k=3):
                enrollment, _ = Enrollment.objects.get_or_create(
                    user=user,
                    course=course
                )
                enrollments.append(enrollment)

        # ------------------------
        # PROGRESS
        # ------------------------
        print("Creating progress...")

        for enrollment in enrollments:
            lessons = enrollment.course.lessons.all()

            for lesson in lessons:
                Progress.objects.get_or_create(
                    user=enrollment.user,
                    lesson=lesson,
                    completed=random.choice([True, False])
                )

        print("🎉 SEEDING DONE (20 STUDENTS)")