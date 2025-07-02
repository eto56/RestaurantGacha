import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Help from './Help';
import './App.css';

function SearchPage() {
  const [station, setStation] = useState('');
  const [genre, setGenre] = useState('');
  const [restaurant, setRestaurant] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRestaurant(null);

    if (!station) {
      setError('駅名は必須です。');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ station, genre }),
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || 'レストランの検索に失敗しました。');
      }

      const data = await response.json();
      if (!data) {
        throw new Error('該当するレストランが見つかりませんでした。');
      }
      setRestaurant(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>restautantGacha</h1>
      <p>お近くのレストランをガチャで見つけよう！</p>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={station}
          onChange={(e) => setStation(e.target.value)}
          placeholder="駅名を入力 (例: 新宿)"
          required
        />
        <input
          type="text"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          placeholder="ジャンルを入力 (任意)(例: 居酒屋)"
        />
        <button type="submit" disabled={loading}>
          {loading ? '検索中...' : 'レストランを探す'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {restaurant && (
        <div className="result">
          <h2>{restaurant.name}</h2>
          <p>{restaurant.kana}</p>
          <a href={restaurant.url} target="_blank" rel="noopener noreferrer">
            ホットペッパーで見る
          </a>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">ホーム</Link> | <Link to="/help">ヘルプ</Link>
      </nav>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/help" element={<Help />} />
      </Routes>
    </Router>
  );
}

export default App;
