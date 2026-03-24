import os
import json
import uuid
from openai import AsyncOpenAI
from models.schemas import Question, QuestionOption
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "dummy_key")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def generate_facts_and_questions(text: str) -> tuple[dict, list[Question]]:
    # 1. Fact Extraction prompt
    system_prompt = \"\"\"You are an expert medical quiz creator. Based ONLY on the provided article text, extract medical facts AND generate 10 multiple-choice questions.

Output must be ONLY valid JSON matching exactly this structure:
{
  "facts": {
    "symptoms": ["..."],
    "causes": ["..."],
    "treatments": ["..."],
    "precautions": ["..."],
    "definitions": ["..."]
  },
  "questions": [
    {
      "text": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_option_index": 0,
      "explanation": "Explanation for the correct answer.",
      "difficulty": "easy",
      "topic_tag": "symptoms"
    }
  ]
}
Make sure you generate questions with varying difficulties ('easy', 'medium', 'hard') and different topic_tags ('symptoms', 'causes', 'treatments', 'precautions', 'definitions').
\"\"\"

    try:
        response = await client.chat.completions.create(
            model="google/gemini-2.5-flash", # Using the latest fast gemini
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Article Text:\n{text[:15000]}"} # limit text size
            ]
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        extracted_facts = data.get("facts", {})
        raw_questions = data.get("questions", [])
        
        questions = []
        for q in raw_questions:
            q_id = str(uuid.uuid4())
            
            question_options = []
            correct_option_id = ""
            for idx, opt_text in enumerate(q.get("options", [])):
                opt_id = str(uuid.uuid4())
                question_options.append(QuestionOption(id=opt_id, text=opt_text))
                if idx == q.get("correct_option_index"):
                    correct_option_id = opt_id
            
            questions.append(Question(
                id=q_id,
                text=q.get("text", "Missing text"),
                options=question_options,
                correct_option_id=correct_option_id,
                explanation=q.get("explanation", ""),
                difficulty=q.get("difficulty", "medium").lower(),
                topic_tag=q.get("topic_tag", "general").lower()
            ))
            
        return extracted_facts, questions
        
    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return {}, []

