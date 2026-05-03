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