import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleIntake from './pages/ArticleIntake';
import QuizInterface from './pages/QuizInterface';
import Results from './pages/Results';

function App() {
  return (
    <Router>
      <div className="navbar">
        <div className="navbar-brand">
          <span style={{color: 'var(--secondary-color)'}}>iCliniq</span> QuizEngine
        </div>
        <div className="nav-links">
          <span>Medical Articles</span>
          <span>Medical Q&A</span>
          <span>Consult a Physician</span>
        </div>
        <button className="consult-btn">Free Consultation</button>
      </div>

      <div className="app-container">
        <Routes>
          <Route path="/" element={<ArticleIntake />} />
          <Route path="/quiz" element={<QuizInterface />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
