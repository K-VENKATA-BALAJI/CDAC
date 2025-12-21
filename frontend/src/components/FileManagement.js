import React, { useState } from 'react';
import axios from 'axios';
import './FileManagement.css';

const FileManagement = ({ specifications, vendors }) => {
  const [fileName, setFileName] = useState('');
  const [fileDescription, setFileDescription] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSave = async (e) => {
    e.preventDefault();
    
    if (!fileName.trim() || !email.trim()) {
      setMessage('Please fill in File Name and Email');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await axios.post('http://localhost:8888/api/save-file', {
        email: email.trim(),
        file_name: fileName.trim(),
        file_description: fileDescription.trim(),
        specifications,
        vendors
      });
      
      setMessage('File saved successfully!');
      setFileName('');
      setFileDescription('');
      setEmail('');
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to save file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-management">
      <form onSubmit={handleSave} className="file-form">
        <div className="form-row-three">
          <div className="form-field">
            <label>File Name:</label>
            <input
              type="text"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              className="form-input"
              placeholder="Enter file name"
            />
          </div>
          
          <div className="form-field">
            <label>File Description:</label>
            <input
              type="text"
              value={fileDescription}
              onChange={(e) => setFileDescription(e.target.value)}
              className="form-input"
              placeholder="Enter file description"
            />
          </div>
          
          <div className="form-field">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-input"
              placeholder="Enter your email"
            />
          </div>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="save-button"
        >
          {loading ? 'Saving...' : 'SAVE'}
        </button>
        
        {message && (
          <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
            {message}
          </div>
        )}
      </form>
    </div>
  );
};

export default FileManagement;


