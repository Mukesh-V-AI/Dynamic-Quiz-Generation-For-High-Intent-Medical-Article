import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BookOpen, Link, AlignLeft } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function ArticleIntake() {
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!url && !text) {
      setError('Please provide either a URL or paste article text.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${API_BASE}/article/process`, { url, text });
      // On success, redirect to quiz using the returned article_id
      navigate('/quiz', { state: { articleId: response.data.article_id, title: response.data.title } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate quiz. Check console.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card">
      {loading && (
        <div className="loading-overlay">
          <div className="loader"></div>
          <h2>AI is reading and generating...</h2>
          <p style={{ color: 'var(--text-secondary)' }}>This may take 15-30 seconds.</p>
        </div>
      )}

      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <BookOpen size={48} color="var(--primary-color)" style={{ marginBottom: '1rem' }} />
        <h1 className="title-gradient">Dynamic MedQuiz Engine</h1>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          Convert any medical article into an adaptive learning experience. Our AI analyzes the text, extracts key facts, and tests your knowledge.
        </p>
      </div>

      {error && <div style={{ color: 'var(--error-color)', marginBottom: '1rem', textAlign: 'center', background: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '8px' }}>{error}</div>}

      <form onSubmit={handleGenerate}>
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', fontWeight: 600 }}>
            <Link size={18} /> Source URL
          </label>
          <input
            type="url"
            className="input-field"
            placeholder="https://example.com/medical-article"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div style={{ textAlign: 'center', margin: '1rem 0', color: 'var(--text-secondary)' }}>— OR —</div>

        <div style={{ marginBottom: '2rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', fontWeight: 600 }}>
            <AlignLeft size={18} /> Raw Article Text
          </label>
          <textarea
            className="input-field"
            placeholder="Paste the medical article text here..."
            rows="6"
            value={text}
            onChange={(e) => setText(e.target.value)}
            style={{ resize: 'vertical' }}
          ></textarea>
        </div>

        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Adaptive Quiz'}
        </button>
      </form>
    </div>
  );
}
