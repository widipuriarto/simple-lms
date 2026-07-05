from ninja import Schema
from typing import Optional, List
from datetime import datetime

class CourseOut(Schema):
    id: int
    title: str
    description: str
    instructor: str
    category: Optional[str]

    @staticmethod
    def resolve_instructor(obj):
        # Jika obj adalah dictionary (dari cache), ambil langsung valuenya. Jika object Django, akses fieldnya.
        if isinstance(obj, dict):
            return obj.get('instructor')
        return obj.instructor.username

    @staticmethod
    def resolve_category(obj):
        if isinstance(obj, dict):
            return obj.get('category')
        return obj.category.name if obj.category else None

class LessonOutSchema(Schema):
    id: int
    title: str
    order: int

class SectionOutSchema(Schema):
    id: int
    title: str
    order: int
    lessons: List[LessonOutSchema]

class CourseDetail(Schema):
    id: int
    title: str
    description: str
    instructor: str
    category: Optional[str]
    level: str
    status: str
    sections: List[SectionOutSchema]  # <--- Ini yang membuat struktur hierarki

class CourseCreateSchema(Schema):
    title: str
    description: str

class CourseFilterSchema(Schema):
    search: Optional[str] = None
    title: Optional[str] = None
    category: Optional[int] = None
    instructor: Optional[str] = None
    level: Optional[str] = None
    status: Optional[str] = None
    ordering: Optional[str] = None

class CourseUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None


class CommentOut(Schema):
    id: int
    user: str
    content: str
    created_at: str

class CommentCreateSchema(Schema):
    content: str


class ReviewOut(Schema):
    id: int
    user: str
    rating: int
    comment: str
    created_at: datetime

    @staticmethod
    def resolve_user(obj):
        return obj.user.username

class ReviewCreateSchema(Schema):
    rating: int
    comment: Optional[str] = ""

class WishlistOut(Schema):
    id: int
    course_id: int
    course_title: str
    created_at: datetime

    @staticmethod
    def resolve_course_id(obj):
        return obj.course.id

    @staticmethod
    def resolve_course_title(obj):
        return obj.course.title

class DashboardCourseSchema(Schema):
    id: int
    title: str
    instructor: str
    progress_percentage: float

class StudentDashboardOut(Schema):
    active_courses: List[DashboardCourseSchema]
    completed_courses: List[DashboardCourseSchema]
    recommended_courses: List[CourseOut]  # Menggunakan CourseOut yang sudah ada



class AdminUserOut(Schema):
    id: int
    username: str
    email: str
    role: str

    @staticmethod
    def resolve_role(obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else 'student'

class AdminEnrollmentOut(Schema):
    id: int
    user: str
    course_title: str
    enrolled_at: datetime

    @staticmethod
    def resolve_user(obj):
        return obj.user.username

    @staticmethod
    def resolve_course_title(obj):
        return obj.course.title

