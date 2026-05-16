from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from courses.models import (
    Category,
    Course,
    Lesson,
    Enrollment,
    Progress,
    UserProfile
)

import random


class Command(BaseCommand):
    help = "Seed dummy data"

    def handle(self, *args, **kwargs):

        # ======================================
        # DELETE OLD DATA
        # ======================================

        print("Deleting old data...")

        Progress.objects.all().delete()
        Enrollment.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Category.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.exclude(username="admin").delete()

        # ======================================
        # USERS
        # ======================================

        print("Creating users...")

        instructors = []
        students = []

        # instructor
        for i in range(5):

            user = User.objects.create_user(
                username=f"instructor{i}",
                password="password123"
            )

            profile, created = UserProfile.objects.get_or_create(
                user=user
            )

            profile.role = "instructor"
            profile.save()

            instructors.append(user)

        # student
        for i in range(15):

            user = User.objects.create_user(
                username=f"student{i}",
                password="password123"
            )

            profile, created = UserProfile.objects.get_or_create(
                user=user
            )

            profile.role = "student"
            profile.save()

            students.append(user)

        # ======================================
        # CATEGORIES
        # ======================================

        print("Creating categories...")

        categories = []

        for i in range(10):

            cat = Category.objects.create(
                name=f"Category {i}"
            )

            categories.append(cat)

        # ======================================
        # COURSES
        # ======================================

        print("Creating courses...")

        courses = []

        for i in range(60):

            course = Course.objects.create(
                title=f"Course {i}",
                description="Lorem ipsum dolor sit amet",
                instructor=random.choice(instructors),
                category=random.choice(categories)
            )

            courses.append(course)

        # ======================================
        # LESSONS
        # ======================================

        print("Creating lessons...")

        lessons = []

        for course in courses:

            for i in range(5):

                lesson = Lesson.objects.create(
                    title=f"{course.title} - Lesson {i}",
                    content="Lesson content",
                    course=course,
                    order=i + 1
                )

                lessons.append(lesson)

        # ======================================
        # ENROLLMENTS
        # ======================================

        print("Creating enrollments...")

        enrollments = []

        for student in students:

            selected_courses = random.sample(courses, 10)

            for course in selected_courses:

                enrollment = Enrollment.objects.create(
                    user=student,
                    course=course
                )

                enrollments.append(enrollment)

        # ======================================
        # PROGRESS
        # ======================================

        print("Creating progress...")

        for enrollment in enrollments:

            course_lessons = enrollment.course.lessons.all()

            for lesson in course_lessons:

                Progress.objects.create(
                    user=enrollment.user,
                    lesson=lesson,
                    completed=random.choice([True, False])
                )

        print("✅ SEEDING DONE!")