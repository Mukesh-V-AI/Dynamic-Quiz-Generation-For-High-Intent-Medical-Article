import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ArticleIntake from './pages/ArticleIntake';
import QuizInterface from './pages/QuizInterface';
import Results from './pages/Results';
import icliniqLogo from './assets/icliniq-logo.png';

function App() {
  return (
    <Router>
      <div className="navbar">
        <Link to="/" className="navbar-brand">
          <img src={icliniqLogo} alt="iCliniq Logo" style={{ height: '40px' }} />
        </Link>
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
