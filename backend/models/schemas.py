from pydantic import BaseModel
from typing import List, Optional, Dict

class ArticleRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None

class ArticleResponse(BaseModel):
    message: str
    article_id: str
    extracted_facts: dict
    title: Optional[str] = None

class QuestionOption(BaseModel):
    id: str
    text: str

class Question(BaseModel):
    id: str
    text: str
    options: List[QuestionOption]
    correct_option_id: str
    explanation: str
    difficulty: str  # easy, medium, hard
    topic_tag: str

class AnswerRequest(BaseModel):
    question_id: str
    selected_option_id: str

class AnswerResponse(BaseModel):
    correct: bool
    correct_option_id: str
    explanation: str
    current_score: int
    streak: int

class QuizResults(BaseModel):
    total_answered: int
    correct_answers: int
    score_percentage: float
    weak_topics: List[str]
