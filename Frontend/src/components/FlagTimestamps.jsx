// src/components/FlagTimestamps.jsx
import React from 'react';

const FlagTimestamps = () => {
  // Sample data - in a real implementation, this would come from your analysis
  const flaggedItems = [
    { time: '00:23', issue: 'Extended silence', severity: 'medium' },
    { time: '01:45', issue: 'Interruption', severity: 'low' },
    { time: '03:12', issue: 'Negative sentiment detected', severity: 'high' },
    { time: '05:34', issue: 'Compliance phrase missing', severity: 'high' },
  ];
  
  return (
    <div className="flag-timestamps">
      <div className="audio-timeline">
        <div className="timeline-track"></div>
        {flaggedItems.map((item, index) => (
          <div 
            key={index} 
            className={`flag-marker ${item.severity}`} 
            style={{ left: `${Math.random() * 80}%` }} // For demo only
          >
            <div className="flag-tooltip">
              <span className="timestamp">{item.time}</span>
              <span className="issue">{item.issue}</span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="flagged-list">
        <h3>Flagged Issues</h3>
        <table className="flags-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Issue</th>
              <th>Severity</th>
            </tr>
          </thead>
          <tbody>
            {flaggedItems.map((item, index) => (
              <tr key={index} className={`severity-${item.severity}`}>
                <td>{item.time}</td>
                <td>{item.issue}</td>
                <td>{item.severity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FlagTimestamps;