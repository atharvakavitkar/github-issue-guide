import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [issueUrl, setIssueUrl] = useState('');
  const [guidance, setGuidance] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('/api/guidance', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ issueUrl }),
      });
      const data = await response.json();
      setGuidance(data.guidance);
    } catch (error) {
      console.error('Error:', error);
      setGuidance('An error occurred while fetching guidance.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>GitHub Issue Guide</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={issueUrl}
          onChange={(e) => setIssueUrl(e.target.value)}
          placeholder="Enter GitHub issue URL"
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Get Guidance'}
        </button>
      </form>
      {guidance && (
        <div className="guidance">
          <ReactMarkdown>{guidance}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;