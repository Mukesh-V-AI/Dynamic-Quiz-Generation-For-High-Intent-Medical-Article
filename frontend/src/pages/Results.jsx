import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Trophy, AlertTriangle, RefreshCw } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const articleId = state?.articleId;
  const title = state?.title;

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!articleId) {
      navigate('/');
      return;
    }
    fetchResults();
  }, [articleId, navigate]);

  const fetchResults = async () => {
    try {
      const res = await axios.get(`${API_BASE}/quiz/${articleId}/results`);
      setResults(res.data);
    } catch (err) {
      console.error("Error fetching results", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
        <div className="loader" style={{ margin: '0 auto 1rem' }}></div>
        <h2>Analyzing your performance...</h2>
      </div>
    );
  }

  if (!results) return null;

  return (
    <div className="glass-card" style={{ textAlign: 'center' }}>
      <Trophy size={64} color="var(--warning-color)" style={{ margin: '0 auto 1.5rem' }} />
      <h1 className="title-gradient" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Quiz Completed!</h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
        {title || 'Your adaptive learning session has ended.'}
      </p>

      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '3rem' }}>
        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', minWidth: '120px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary-color)' }}>
            {results.percentage?.toFixed(0) || Math.round(results.score_percentage)}%
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Accuracy</div>
        </div>
        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '12px', minWidth: '120px' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--success-color)' }}>
            {results.correct_answers} / {results.total_answered}
          </div>
          <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>Correct</div>
        </div>
      </div>

      {results.weak_topics && results.weak_topics.length > 0 && (
        <div style={{ background: 'rgba(239, 68, 68, 0.05)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: '1.5rem', borderRadius: '12px', textAlign: 'left', marginBottom: '2rem' }}>
          <h3 style={{ color: 'var(--error-color)', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: 0 }}>
            <AlertTriangle size={20} /> Needs Improvement
          </h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
            Based on your answers, you should review the following topics:
          </p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {results.weak_topics.map(topic => (
              <span key={topic} className="badge badge-topic" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#f87171' }}>
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      <button className="btn" onClick={() => navigate('/')}>
        <RefreshCw size={20} /> Generate Another Quiz
      </button>
    </div>
  );
}
