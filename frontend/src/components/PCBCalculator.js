import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './PCBCalculator.css';
import PCBSpecifications from './PCBSpecifications';
import PCBRates from './PCBRates';
import FileManagement from './FileManagement';

const PCBCalculator = ({ loadedData, onNewFile, onLoadFile }) => {
  const [specifications, setSpecifications] = useState({});
  const [specOptions, setSpecOptions] = useState({});
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showFileMenu, setShowFileMenu] = useState(false);
  const [showEmailPopup, setShowEmailPopup] = useState(false);
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [emailLoading, setEmailLoading] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    // Load specification options from backend
    loadSpecifications();
    
    // If loaded data exists, populate the form
    if (loadedData && loadedData.specifications) {
      setSpecifications(loadedData.specifications);
      if (loadedData.vendors && loadedData.vendors.length > 0) {
        setVendors(loadedData.vendors);
      }
    }
  }, [loadedData]);

  useEffect(() => {
    // Close menu when clicking outside
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowFileMenu(false);
      }
    };

    if (showFileMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showFileMenu]);

  const loadSpecifications = async () => {
    try {
      const response = await axios.get('http://localhost:8888/api/specifications');
      setSpecOptions(response.data);
      
      // Initialize default values
      const defaults = {};
      Object.keys(response.data).forEach(key => {
        if (response.data[key].length > 0) {
          defaults[key] = response.data[key][0];
        }
      });
      
      if (!loadedData) {
        setSpecifications(defaults);
      }
    } catch (err) {
      setError('Failed to load specifications');
      console.error(err);
    }
  };

  const handleSpecificationChange = (field, value) => {
    setSpecifications(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleCalculateRates = async () => {
    setLoading(true);
    setError('');
    
    try {
      console.log('Sending specifications:', specifications);
      const response = await axios.post('http://localhost:8888/api/calculate-rates', {
        specifications
      });
      console.log('Received response:', response.data);
      setVendors(response.data);
      
      if (!response.data || response.data.length === 0) {
        setError('No rates found for the selected specifications. Please try different values.');
      }
    } catch (err) {
      console.error('Error calculating rates:', err);
      setError(err.response?.data?.error || 'Failed to calculate rates. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileMenuClick = () => {
    setShowFileMenu(!showFileMenu);
  };

  const handleNewFileClick = () => {
    onNewFile();
    setShowFileMenu(false);
    setVendors([]);
  };

  const handleLoadFileClick = () => {
    setShowFileMenu(false);
    setShowEmailPopup(true);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setEmailError('Please enter an email address');
      return;
    }

    setEmailLoading(true);
    setEmailError('');

    try {
      const response = await axios.post('http://localhost:8888/api/load-file', {
        email: email.trim()
      });

      if (response.data.success && response.data.data && response.data.data.length > 0) {
        onLoadFile(response.data.data[0]);
        setShowEmailPopup(false);
        setEmail('');
      } else {
        setEmailError('No files found for this email');
      }
    } catch (err) {
      setEmailError(err.response?.data?.error || 'Failed to load file');
    } finally {
      setEmailLoading(false);
    }
  };

  return (
    <div className="pcb-calculator">
      <div className="header">
        <div className="file-menu-container" ref={menuRef}>
          <span className="file-menu-trigger" onClick={handleFileMenuClick}>File</span>
          {showFileMenu && (
            <div className="file-menu-dropdown">
              <div className="file-menu-item" onClick={handleNewFileClick}>New File</div>
              <div className="file-menu-item" onClick={handleLoadFileClick}>Load File</div>
            </div>
          )}
        </div>
      </div>
      <div className="container">
        {error && <div className="error-banner">{error}</div>}
        
        <div className="calculator-layout">
          <div className="specifications-section">
            <PCBSpecifications
              specifications={specifications}
              specOptions={specOptions}
              onChange={handleSpecificationChange}
              onCalculate={handleCalculateRates}
              loading={loading}
            />
          </div>
          
          <div className="rates-section">
            <PCBRates vendors={vendors} />
          </div>
        </div>
        
        <div className="file-management-section">
          <FileManagement
            specifications={specifications}
            vendors={vendors}
          />
        </div>
      </div>

      {showEmailPopup && (
        <div className="email-popup-overlay" onClick={() => setShowEmailPopup(false)}>
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
              {emailError && <div className="error-message">{emailError}</div>}
              <div className="popup-buttons">
                <button type="button" onClick={() => setShowEmailPopup(false)} className="cancel-btn">
                  Cancel
                </button>
                <button type="submit" disabled={emailLoading} className="submit-btn">
                  {emailLoading ? 'Loading...' : 'Load'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PCBCalculator;


