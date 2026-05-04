import React, { useState, useEffect } from 'react';
import { X, AlertCircle, TrendingUp, Users, Activity, Loader } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import '../styles/SidePanel.css';

const SidePanel = ({ conflict, onClose }) => {
  const [news, setNews] = useState([]);
  const [loadingNews, setLoadingNews] = useState(true);
  const [newsError, setNewsError] = useState(null);

  useEffect(() => {
    fetchNews();
  }, [conflict]);

  const fetchNews = async () => {
    setLoadingNews(true);
    setNewsError(null);
    try {
      const response = await fetch(
        `http://localhost:5001/api/conflicts/${conflict.id}/news`
      );
      const data = await response.json();
      setNews(data.articles || []);
    } catch (error) {
      console.error('Error fetching news:', error);
      setNewsError('Failed to load news articles');
      setNews([]);
    } finally {
      setLoadingNews(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        className="side-panel"
        initial={{ x: 400, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 400, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        {/* Close Button */}
        <button className="close-button" onClick={onClose} aria-label="Close panel">
          <X size={24} />
        </button>

        {/* Conflict Header */}
        <div className="panel-header">
          <div className="conflict-title-section">
            <h2 className="conflict-title">{conflict.name}</h2>
            <div className="conflict-location">
              📍 {conflict.country}
            </div>
          </div>
          <div className={`status-badge status-${conflict.status.toLowerCase().replace(/\s+/g, '-')}`}>
            {conflict.status}
          </div>
        </div>

        {/* Conflict Description */}
        <div className="panel-section">
          <p className="description">{conflict.description}</p>
        </div>

        {/* Key Statistics */}
        <div className="panel-section">
          <h3 className="section-title">Key Statistics</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <Activity size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Intensity</div>
                <div className="stat-value">{conflict.intensity}/10</div>
                <div className="intensity-bar">
                  <div
                    className="intensity-fill"
                    style={{
                      width: `${conflict.intensity * 10}%`,
                      backgroundColor: getIntensityColor(conflict.intensity)
                    }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <AlertCircle size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Estimated Deaths</div>
                <div className="stat-value">
                  {(conflict.estimatedDeaths / 1000).toFixed(0)}K+
                </div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <Users size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Parties Involved</div>
                <div className="stat-value">{conflict.parties.length}</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <TrendingUp size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-label">Since</div>
                <div className="stat-value">
                  {new Date(conflict.startDate).getFullYear()}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Parties Involved */}
        <div className="panel-section">
          <h3 className="section-title">Parties Involved</h3>
          <div className="parties-list">
            {conflict.parties.map((party, idx) => (
              <span key={idx} className="party-badge">
                {party}
              </span>
            ))}
          </div>
        </div>

        {/* Main Causes */}
        <div className="panel-section">
          <h3 className="section-title">Main Causes</h3>
          <p className="causes-text">{conflict.mainCauses}</p>
        </div>

        {/* International Response */}
        <div className="panel-section">
          <h3 className="section-title">International Response</h3>
          <p className="response-text">{conflict.internationalResponse}</p>
        </div>

        {/* Latest News */}
        <div className="panel-section news-section">
          <h3 className="section-title">Latest News</h3>
          {loadingNews ? (
            <div className="loading-news">
              <Loader size={20} className="spinner" />
              <span>Fetching latest articles...</span>
            </div>
          ) : newsError ? (
            <div className="news-error">{newsError}</div>
          ) : news.length > 0 ? (
            <div className="news-list">
              {news.map((article, idx) => (
                <motion.a
                  key={idx}
                  href={article.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="news-article"
                  whileHover={{ translateX: 4 }}
                  transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                >
                  <div className="news-header">
                    <span className="news-source">{article.source}</span>
                    <span className="news-date">{formatDate(article.published)}</span>
                  </div>
                  <h4 className="news-title">{article.title}</h4>
                  {article.summary && (
                    <p className="news-summary">{article.summary}</p>
                  )}
                </motion.a>
              ))}
            </div>
          ) : (
            <div className="no-news">No articles found for this conflict</div>
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

const getIntensityColor = (intensity) => {
  if (intensity >= 8) return '#dc2626';
  if (intensity >= 6) return '#ea580c';
  if (intensity >= 4) return '#f59e0b';
  return '#fbbf24';
};

export default SidePanel;
