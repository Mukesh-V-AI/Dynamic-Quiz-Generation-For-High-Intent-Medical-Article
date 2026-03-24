from typing import List, Optional
from models.schemas import Question, AnswerResponse, QuizResults

class QuizEngine:
    def __init__(self, questions: List[Question]):
        self.all_questions = questions
        self.available_questions = {q.id: q for q in questions}
        
        self.user_answers = []
        self.current_score = 0
        self.streak = 0
        
        self.current_difficulty = "medium"  # starts at medium
        self.topic_stats = {} # {"symptoms": {"total": 0, "correct": 0}}
        
    def get_next_question(self) -> Optional[Question]:
        if not self.available_questions:
            return None
            
        # 1. Try to find a question matching current target difficulty and a weak topic
        weak_topics = self._get_weak_topics()
        
        for q_id, q in list(self.available_questions.items()):
            if q.topic_tag in weak_topics and q.difficulty == self.current_difficulty:
                return q
        
        # 2. Relax weak topic constraint, just match difficulty
        for q_id, q in list(self.available_questions.items()):
            if q.difficulty == self.current_difficulty:
                return q
                
        # 3. Relax all constraints, return any available question
        return list(self.available_questions.values())[0]

    def _get_weak_topics(self) -> List[str]:
        weak_topics = []
        for topic, stats in self.topic_stats.items():
            if stats["total"] > 0:
                accuracy = stats["correct"] / stats["total"]
                if accuracy <= 0.5:
                    weak_topics.append(topic)
        return weak_topics

    def submit_answer(self, question_id: str, selected_option_id: str) -> AnswerResponse:
        if question_id not in self.available_questions:
            raise ValueError("Question not available or already answered")
            
        q = self.available_questions.pop(question_id)
        
        is_correct = (selected_option_id == q.correct_option_id)
        self.user_answers.append({"question_id": question_id, "correct": is_correct, "topic": q.topic_tag})
        
        # Update topic stats
        if q.topic_tag not in self.topic_stats:
            self.topic_stats[q.topic_tag] = {"total": 0, "correct": 0}
        self.topic_stats[q.topic_tag]["total"] += 1
        
        if is_correct:
            self.current_score += 10
            self.streak += 1
            self.topic_stats[q.topic_tag]["correct"] += 1
            
            # Difficulty progression up
            if self.current_difficulty == "easy":
                self.current_difficulty = "medium"
            elif self.current_difficulty == "medium":
                self.current_difficulty = "hard"
        else:
            self.streak = 0
            # Difficulty progression down
            if self.current_difficulty == "hard":
                self.current_difficulty = "medium"
            elif self.current_difficulty == "medium":
                self.current_difficulty = "easy"
                
        return AnswerResponse(
            correct=is_correct,
            correct_option_id=q.correct_option_id,
            explanation=q.explanation,
            current_score=self.current_score,
            streak=self.streak
        )

    def get_results(self) -> QuizResults:
        total = len(self.user_answers)
        correct = sum(1 for ans in self.user_answers if ans["correct"])
        percentage = (correct / total * 100) if total > 0 else 0
        
        return QuizResults(
            total_answered=total,
            correct_answers=correct,
            score_percentage=percentage,
            weak_topics=self._get_weak_topics()
        )
