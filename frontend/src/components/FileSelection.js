import React, { useState } from 'react';
import axios from 'axios';
import './FileSelection.css';

const FileSelection = ({ onNewFile, onLoadFile }) => {
  const [showEmailInput, setShowEmailInput] = useState(false);
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLoadFile = async () => {
    setShowEmailInput(true);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError('Please enter an email address');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8888/api/load-file', {
        email: email.trim()
      });

      if (response.data.success && response.data.data && response.data.data.length > 0) {
        // If multiple files, show selection (for now, take first one)
        onLoadFile(response.data.data[0]);
      } else {
        setError('No files found for this email');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-selection">
      <div className="header">File</div>
      <div className="selection-container">
        <div className="selection-card" onClick={onNewFile}>
          <div className="card-icon">📄</div>
          <h2>New File</h2>
          <p>Create a new PCB specification and calculate rates</p>
        </div>
        
        <div className="selection-card" onClick={handleLoadFile}>
          <div className="card-icon">📂</div>
          <h2>Load File</h2>
          <p>Load an existing PCB specification file</p>
        </div>
      </div>

      {showEmailInput && (
        <div className="email-popup-overlay" onClick={() => setShowEmailInput(false)}>
          <div className="email-popup" onClick={(e) => e.stopPropagation()}>
            <h3>Enter Email Address</h3>
            <form onSubmit={handleEmailSubmit}>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="email-input"
                autoFocus
              />
              {error && <div className="error-message">{error}</div>}
              <div className="popup-buttons">
                <button type="button" onClick={() => setShowEmailInput(false)} className="cancel-btn">
                  Cancel
                </button>
                <button type="submit" disabled={loading} className="submit-btn">
                  {loading ? 'Loading...' : 'Load'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileSelection;


