import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleIntake from './pages/ArticleIntake';
import QuizInterface from './pages/QuizInterface';
import Results from './pages/Results';

function App() {
  return (
    <Router>
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
