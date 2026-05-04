import React, { useState, useEffect } from 'react';
import GlobeComponent from './components/Globe';
import SidePanel from './components/SidePanel';
import Header from './components/Header';
import './styles/App.css';

function App() {
  const [selectedConflict, setSelectedConflict] = useState(null);
  const [conflicts, setConflicts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchConflicts();
    fetchStats();
  }, []);

  const fetchConflicts = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/conflicts');
      const data = await response.json();
      setConflicts(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching conflicts:', error);
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className="app">
      <Header stats={stats} />
      <div className="main-container">
        <GlobeComponent 
          conflicts={conflicts} 
          onSelectConflict={setSelectedConflict}
          selectedConflict={selectedConflict}
        />
        {selectedConflict && (
          <SidePanel 
            conflict={selectedConflict} 
            onClose={() => setSelectedConflict(null)}
          />
        )}
      </div>
    </div>
  );
}

export default App;
