# Dynamic Quiz Generation - Project Overview

This document summarizes the work completed, the technologies used, and the roadmap for future optimizations.

## 1. Accomplishments (What has been Done)

### Backend (FastAPI + Python)
- **Article Extraction Engine**: Implemented using `BeautifulSoup4` and `httpx` to scrape and clean medical content from URLs or raw text.
- **Adaptive Quiz Logic**: Developed a custom `QuizEngine` that:
  - Tracks user score and current streak.
  - Dynamically identifies "weak topics" based on incorrect answers.
  - Adapts difficulty (Easy/Medium/Hard) based on user performance.
- **LLM Integration (OpenRouter)**: Integrated with the **MiniMax-01** model (OpenRouter) with specialized JSON-cleaning logic and token-limit management (fixed the 402/401 errors).
- **In-Memory Storage**: Current session state is managed via an in-memory dictionary for ultra-fast MVP performance.

### Frontend (React + Vite)
- **iCliniq Brand-Themed UI**: Custom CSS implementation matching the iCliniq deep-blue and cyan-plus aesthetic.
- **Interactive Quiz Interface**: Responsive MCQ component with immediate feedback and explanation for each question.
- **Analytics Dashboard**: Results page showing accuracy, score, and categorized "Weak Topics" to guide further learning.
- **Branding**: Integrated official iCliniq logo and simplified the navigation for a focused user experience.

---

## 2. Technical Decisions & Current State

### Database Status
- **Current**: **In-Memory Storage**. 
- **Rationale**: Used for rapid prototyping and zero-latency session management. It ensures the environment stays lightweight without needing a database setup locally.
- **Limitation**: State (sessions) is lost when the backend server restarts.

### Git Repository
- Successfully initialized and pushed to: `https://github.com/Mukesh-V-AI/Dynamic-Quiz-Generation-For-High-Inent-Medical-Article.git`

---

## 3. Roadmap for Optimal Low Latency (Reducing Generation Time)

To significantly reduce the current ~10-15s generation time, the following technical strategies are recommended:

### A. Server-Sent Events (SSE) Streaming
- **Implementation**: Modify the FastAPI backend to use `StreamingResponse` and the OpenAI `stream=True` parameter.
- **Impact**: Instead of waiting 10 seconds for a full JSON block, questions will appear one-by-one as the AI thinks. The user sees the first question in **< 2 seconds**.

### B. Intelligent Response Caching (Redis)
- **Implementation**: Store previously generated quizzes for common medical URLs in a Redis cache.
- **Impact**: If another user requests the same article, the response is **Instant (0ms generation time)**.

### C. Parallelization of Sub-Tasks
- **Implementation**: Split the single large prompt into two parallel calls: one for Fact Extraction and one for Question Generation.
- **Impact**: Processing both at once can shave off 30-40% of the total execution time.

### D. Model Selection (Gemini 2.0 Flash)
- **Implementation**: Switch from `minimax-01` to `google/gemini-2.0-flash`.
- **Impact**: Gemini 2.0 Flash is specifically optimized for ultra-low latency and higher throughput, typically being **2x-3x faster** than minimax for large JSON outputs.

### E. Prompt Compression & Concise System Prompts
- **Implementation**: Minify the "System Prompt" and use few-shot examples to guide the AI to skip polite chatter and output bare JSON immediately.
- **Impact**: Fewer "Reasoning" tokens produced by the AI results in faster final delivery.
