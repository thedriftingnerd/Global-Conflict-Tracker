import React from 'react';
import { Globe, AlertCircle } from 'lucide-react';
import '../styles/Header.css';

const Header = ({ stats }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo">
            <Globe size={28} />
          </div>
          <h1 className="app-title">Conflict Tracker</h1>
          <p className="app-subtitle">Real-time monitoring of global conflicts</p>
        </div>

        {stats && (
          <div className="stats-summary">
            <div className="stat-item">
              <span className="stat-label">Active Conflicts</span>
              <span className="stat-number">{stats.activeConflicts}</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <span className="stat-label">Total Tracked</span>
              <span className="stat-number">{stats.totalConflicts}</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <span className="stat-label">Avg Intensity</span>
              <span className="stat-number">{stats.averageIntensity}</span>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
