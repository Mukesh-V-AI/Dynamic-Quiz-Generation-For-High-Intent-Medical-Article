import os
import json
import uuid
from openai import AsyncOpenAI
from models.schemas import Question, QuestionOption
from dotenv import load_dotenv

load_dotenv(override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "dummy_key")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def generate_facts_and_questions(text: str) -> tuple[dict, list[Question]]:
    # 1. Fact Extraction and Question Generation prompt
    system_prompt = """You are an expert medical quiz creator. Based ONLY on the provided article text, extract medical facts AND generate 10 questions.

To keep the quiz engaging, use a variety of question formats:
1. **Multiple Choice**: Standard 4-option question.
2. **True/False**: 2-option question (True or False).
3. **Clinical Scenarios**: Create a brief "case study" scenario (e.g., "A patient presents with...") based on the article's facts, followed by a question.

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
      "text": "Question text here (can include a clinical scenario).",
      "options": ["Option A", "Option B", ...],
      "correct_option_index": 0,
      "explanation": "Explanation for the correct answer.",
      "difficulty": "easy",
      "topic_tag": "symptoms"
    }
  ]
}
Make sure you generate questions with varying difficulties ('easy', 'medium', 'hard') and different topic_tags ('symptoms', 'causes', 'treatments', 'precautions', 'definitions'). Ensure a mix of T/F, Scenarios, and Standard MCQs.
"""

    try:
        response = await client.chat.completions.create(
            model="minimax/minimax-01", # Set to MiniMax per user request
            # response_format={"type": "json_object"}, # Removed for compatibility
            max_tokens=4000, # Explicitly limit tokens to avoid 402 "affordability" errors
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Article Text:\n{text[:15000]}"} # limit text size
            ]
        )
        
        content = response.choices[0].message.content
        
        # Clean markdown code block if present
        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        elif clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
            
        try:
            data = json.loads(clean_content.strip())
        except json.JSONDecodeError as je:
            print(f"JSON Parsing Error: {je}")
            print(f"Attempting to manually extract JSON from content...")
            # Fallback: find first { and last }
            start = clean_content.find('{')
            end = clean_content.rfind('}')
            if start != -1 and end != -1:
                try:
                    data = json.loads(clean_content[start:end+1])
                except:
                    print("Fallback JSON parsing failed.")
                    return {}, []
            else:
                return {}, []
        
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

