from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from courses.models import (
    Category,
    Course,
    Section,
    Lesson,
    Enrollment,
    Progress,
    UserProfile,
    Review,
    Wishlist
)

import random


class Command(BaseCommand):
    help = "Seed dummy data"

    def handle(self, *args, **kwargs):

        # ======================================
        # DELETE OLD DATA
        # ======================================

        print("Deleting old data...")

        Wishlist.objects.all().delete()
        Review.objects.all().delete()
        Progress.objects.all().delete()
        Enrollment.objects.all().delete()
        Lesson.objects.all().delete()
        Section.objects.all().delete()
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

        levels = ['beginner', 'intermediate', 'advanced']
        statuses = ['draft', 'published', 'published'] # Mayoritas published agar muncul di endpoint

        for i in range(60):

            course = Course.objects.create(
                title=f"Course {i}",
                description="Lorem ipsum dolor sit amet",
                instructor=random.choice(instructors),
                category=random.choice(categories),
                level=random.choice(levels),
                status=random.choice(statuses)
            )

            courses.append(course)

        # ======================================
        # LESSONS
        # ======================================

        print("Creating sections & lessons...")

        lessons = []

        for course in courses:
            # Buat 3 section untuk tiap course
            for s in range(3):
                section = Section.objects.create(
                    title=f"Section {s + 1} of {course.title}",
                    course=course,
                    order=s + 1
                )
                
                # Buat 4 lesson untuk tiap section
                for i in range(4):
                    lesson = Lesson.objects.create(
                        title=f"{section.title} - Lesson {i + 1}",
                        content="Lesson content",
                        course=course,
                        section=section,
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

        # ======================================
        # REVIEWS & WISHLISTS
        # ======================================

        print("Creating reviews & wishlists...")
        
        for student in students:
            enrolled_courses = [e.course for e in Enrollment.objects.filter(user=student)]
            reviewed_courses = random.sample(enrolled_courses, min(3, len(enrolled_courses)))
            
            for course in reviewed_courses:
                Review.objects.create(
                    user=student,
                    course=course,
                    rating=random.randint(3, 5),
                    comment="Materi kursus ini sangat bagus dan terstruktur!"
                )
            
            not_enrolled = [c for c in courses if c not in enrolled_courses]
            wishlist_courses = random.sample(not_enrolled, min(4, len(not_enrolled)))
            
            for course in wishlist_courses:
                Wishlist.objects.create(
                    user=student,
                    course=course
                )

        print("✅ SEEDING DONE!")