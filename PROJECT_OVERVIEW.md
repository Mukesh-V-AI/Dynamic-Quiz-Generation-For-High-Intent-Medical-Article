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

## 3. Roadmap for Optimal Low Latency Quiz Generation

To take the "Low Latency" to a production level, the following optimizations are recommended:

### A. LLM Response Streaming
- **Action**: Switch from a single blocking request to **Server-Sent Events (SSE)**.
- **Impact**: Questions appearing one-by-one as the AI thinks, reducing perceived "Waiting" time from ~10s to <1s.

### B. Intelligent Caching (Redis)
- **Action**: Implement Redis to cache generated quizzes for popular URLs.
- **Impact**: Instant (millisecond) delivery of quizzes for previously seen articles, bypassing LLM generation entirely.

### C. Persistent Database (MongoDB / Atlas)
- **Action**: Migrate In-Memory sessions to **MongoDB**.
- **Impact**: Persistent user history, long-term learning analytics, and the ability to scale to thousands of simultaneous users.

### D. Asynchronous Background Tasks (Celery)
- **Action**: Move article scraping and fact extraction to a background worker.
- **Impact**: The UI remains responsive immediately while the backend works in the background.

### E. Global CDN & Edge Functions
- **Action**: Deploy the frontend to Vercel/Netlify and the backend to an Edge-compatible server (like Fly.io).
- **Impact**: Reduces network round-trip time for users globally.
