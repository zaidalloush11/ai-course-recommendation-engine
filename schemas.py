from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    user_id: Optional[int] = None
    user_text: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    similarity_score: float

class RecommendResponse(BaseModel):
    extracted_skills: List[str]
    recommended_courses: List[CourseResponse]
    explanation: str