from fastapi import APIRouter, HTTPException
from models.schemas import ArticleRequest, ArticleResponse, Question, AnswerRequest, AnswerResponse, QuizResults
from services.article_service import extract_article_content
from services.llm_service import generate_facts_and_questions
from services.quiz_engine import QuizEngine
import uuid

router = APIRouter()

# In-memory storage for MVP (replacing MongoDB)
articles_db = {}
quizzes_db = {}
user_sessions = {}

@router.post("/article/process", response_model=ArticleResponse)
async def process_article(req: ArticleRequest):
    if not req.url and not req.text:
        raise HTTPException(status_code=400, detail="Must provide url or text")
    
    # 1. Extract content
    content, title = extract_article_content(req.url, req.text)
    
    if content.startswith("Error"):
        raise HTTPException(status_code=400, detail=f"Could not extract article: {content}")
        
    # 2. Extract facts and generate questions using OpenRouter
    facts, questions = await generate_facts_and_questions(content)
    
    if not questions:
        raise HTTPException(status_code=500, detail="The AI failed to generate any valid questions from this article. Try a different article or paste the raw text.")
    
    article_id = str(uuid.uuid4())
    articles_db[article_id] = {"title": title, "content": content, "facts": facts}
    quizzes_db[article_id] = questions
    
    # Initialize a new quiz session for this article
    session_id = article_id # For simple MVP we use article_id as session_id
    user_sessions[session_id] = QuizEngine(questions)
    
    return ArticleResponse(
        message="Article processed successfully",
        article_id=article_id,
        extracted_facts=facts,
        title=title
    )

@router.get("/quiz/{article_id}/next", response_model=Question)
async def get_next_question(article_id: str):
    if article_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Quiz session not found")
        
    engine = user_sessions[article_id]
    question = engine.get_next_question()
    
    if not question:
        raise HTTPException(status_code=404, detail="No more questions available")
        
    # Remove correct option so frontend doesn't cheat
    safe_question = question.model_copy()
    safe_question.correct_option_id = "" 
    safe_question.explanation = ""
    return safe_question

@router.post("/quiz/{article_id}/answer", response_model=AnswerResponse)
async def submit_answer(article_id: str, answer: AnswerRequest):
    if article_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Quiz session not found")
        
    engine = user_sessions[article_id]
    result = engine.submit_answer(answer.question_id, answer.selected_option_id)
    return result

@router.get("/quiz/{article_id}/results", response_model=QuizResults)
async def get_quiz_results(article_id: str):
    if article_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Quiz session not found")
        
    engine = user_sessions[article_id]
    return engine.get_results()
