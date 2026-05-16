from ninja import Schema
from typing import Optional, List

class CourseOut(Schema):
    id: int
    title: str
    description: str
    instructor: str
    category: Optional[str]

class CourseDetail(Schema):
    id: int
    title: str
    description: str
    instructor: str
    category: Optional[str]
    lessons: List[str]

class CourseCreateSchema(Schema):
    title: str
    description: str

class CourseFilterSchema(Schema):
    title: Optional[str] = None
    category: Optional[int] = None
    instructor: Optional[str] = None
    ordering: Optional[str] = None

class CourseUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None





