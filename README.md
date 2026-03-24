# Dynamic Quiz Generation Engine

An end-to-end full-stack application that transforms any medical article into an interactive, adaptive quiz using cutting-edge LLMs via OpenRouter.

## Features
- 🚀 **FastAPI Backend**: Asynchronous extraction and quiz logic handling.
- 🎨 **React + Vite Frontend**: Modern glass-morphic UI with vanilla CSS.
- 🧠 **AI Integration**: Connects to OpenRouter to use Gemini-2.5-Flash (or any model) for extracting medical facts and generating multiple-choice questions.
- 📈 **Adaptive Logic**: Automatically adjusts question difficulty based on your streak and identifies weak topics for improvement.

## Prerequisites
- Node.js (v18+)
- Python 3.9+
- An [OpenRouter API Key](https://openrouter.ai/)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd Dynamic-Quiz-Generation
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```
OPENROUTER_API_KEY=your_key_here
```

Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```
> The API will be available at `http://localhost:8000`

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
> The application will be available at `http://localhost:5173`

## Usage
1. Open the frontend URL in your browser.
2. Paste a link to a valid medical article (e.g. Mayo Clinic, WebMD) or paste raw article text.
3. Click **Generate Adaptive Quiz**. 
4. Begin the test! The engine will keep track of your performance.

## License
MIT License
