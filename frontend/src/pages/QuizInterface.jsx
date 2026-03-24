import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { CheckCircle2, XCircle, ChevronRight, Activity } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function QuizInterface() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const articleId = state?.articleId;
  const title = state?.title;

  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedOption, setSelectedOption] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [stats, setStats] = useState({ score: 0, streak: 0 });

  useEffect(() => {
    if (!articleId) {
      navigate('/');
      return;
    }
    fetchNextQuestion();
  }, [articleId, navigate]);

  const fetchNextQuestion = async () => {
    setLoading(true);
    setSelectedOption(null);
    setFeedback(null);
    try {
      const res = await axios.get(`${API_BASE}/quiz/${articleId}/next`);
      setQuestion(res.data);
    } catch (err) {
      if (err.response?.status === 404) {
        // No more questions, go to results
        navigate('/results', { state: { articleId, title } });
      } else {
        console.error("Error fetching question", err);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOptionClick = async (optionId) => {
    if (feedback) return; // Prevent multiple clicks
    setSelectedOption(optionId);
    setLoading(true);
    
    try {
      const res = await axios.post(`${API_BASE}/quiz/${articleId}/answer`, {
        question_id: question.id,
        selected_option_id: optionId
      });
      setFeedback(res.data);
      setStats({ score: res.data.current_score, streak: res.data.streak });
    } catch (err) {
      console.error("Error submitting answer:", err);
    } finally {
      setLoading(false);
    }
  };

  const finishQuiz = () => {
     navigate('/results', { state: { articleId, title } });
  }

  if (loading && !question) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div className="loader" style={{ margin: '0 auto 1rem' }}></div>
        <h2>Loading next intelligent question...</h2>
      </div>
    );
  }

  if (!question) return null;

  return (
    <div className="glass-card">
      <div className="header-stats">
        <div>
          <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Current Score</span>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>{stats.score}</div>
        </div>
        <div>
          <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Streak 🔥</span>
          <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--warning-color)' }}>{stats.streak}</div>
        </div>
        <button className="btn" style={{ width: 'auto', padding: '0.5rem 1rem', background: 'transparent', border: '1px solid rgba(255,255,255,0.2)' }} onClick={finishQuiz}>
          Finish Early
        </button>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <span className={`badge badge-${question.difficulty}`}>
          {question.difficulty}
        </span>
        <span className="badge badge-topic">
          {question.topic_tag}
        </span>
      </div>

      <h2 style={{ fontSize: '1.25rem', lineHeight: 1.6, marginBottom: '2rem' }}>
        {question.text}
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {question.options.map((opt) => {
          let className = "option-btn";
          if (feedback) {
            if (opt.id === feedback.correct_option_id) {
              className += " correct";
            } else if (opt.id === selectedOption && !feedback.correct) {
              className += " incorrect";
            }
          } else if (selectedOption === opt.id) {
            className += " selected";
          }

          return (
            <button
              key={opt.id}
              className={className}
              onClick={() => handleOptionClick(opt.id)}
              disabled={!!feedback || loading}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>{opt.text}</span>
                {feedback && opt.id === feedback.correct_option_id && <CheckCircle2 size={20} color="var(--success-color)" />}
                {feedback && opt.id === selectedOption && !feedback.correct && <XCircle size={20} color="var(--error-color)" />}
              </div>
            </button>
          );
        })}
      </div>

      {feedback && (
        <div className="explanation-box" style={{ borderColor: feedback.correct ? 'var(--success-color)' : 'var(--error-color)' }}>
          <h3 style={{ color: feedback.correct ? 'var(--success-color)' : 'var(--error-color)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {feedback.correct ? <CheckCircle2 size={24} /> : <XCircle size={24} />}
            {feedback.correct ? 'Correct!' : 'Incorrect'}
          </h3>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            {feedback.explanation}
          </p>
          
          <button 
            className="btn" 
            style={{ marginTop: '1.5rem' }}
            onClick={fetchNextQuestion}
          >
            Next Question <ChevronRight size={20} />
          </button>
        </div>
      )}
    </div>
  );
}
