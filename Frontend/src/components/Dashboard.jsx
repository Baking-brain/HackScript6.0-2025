import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';
import AudioUploader from './AudioUploader';
import ToneGraph from './ToneGraph';
import FlagTimestamps from './FlagTimestamps';

const Dashboard = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  
  const handleAudioUpload = (file) => {
    setAudioFile(file);
    // In a real implementation, you would process the audio file here
  };

  // Toggle theme function
  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  // Apply theme class to document body when theme changes
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }, [darkMode]);

  return (
    <div className="dashboard-container">
      <div className="header-section">
        <div className="header-content">
          <h1>QA-BOT Voice Agent Analyzer</h1>
          <div className="theme-toggle-container">
            <label className="switch">
              <input 
                type="checkbox" 
                checked={darkMode} 
                onChange={toggleTheme} 
              />
              <span className="slider round"></span>
            </label>
            <span className="toggle-label">{darkMode ? 'Dark Mode' : 'Light Mode'}</span>
          </div>
        </div>
      </div>
      
      <div className="upload-section">
        <AudioUploader onUpload={handleAudioUpload} />
      </div>
      
      <div className="graphs-section">
        <div className="tone-graphs">
          <div className="graph-card">
            <h2>Agent Tone Analysis</h2>
            <ToneGraph id="agent-tone" />
          </div>
          
          <div className="graph-card">
            <h2>Customer Sentiment Analysis</h2>
            <ToneGraph id="customer-sentiment" />
          </div>
        </div>
        
        <div className="timestamps-section">
          <div className="timestamps-card">
            <h2>Call Flagged Timestamps</h2>
            <FlagTimestamps />
          </div>
        </div>
      </div>
      
      <div className="metrics-section">
        <h2>Performance Metrics</h2>
        <div className="metrics-cards">
          <div className="metric-card">
            <h3>Response Time</h3>
            <p className="metric-value">1.4s</p>
          </div>
          <div className="metric-card">
            <h3>Accuracy</h3>
            <p className="metric-value">92%</p>
          </div>
          <div className="metric-card">
            <h3>Overall Sentiment</h3>
            <p className="metric-value">Positive</p>
          </div>
          <div className="metric-card">
            <h3>Compliance</h3>
            <p className="metric-value">98%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;