import React from 'react';
import './PCBSpecifications.css';

const PCBSpecifications = ({ specifications, specOptions, onChange, onCalculate, loading }) => {
  // Field mapping: Internal name -> Display name
  const fieldLabels = {
    'PCB Material': 'PCB Material',
    'PCB Finish': 'PCB Finish',
    'Copper Thickness': 'Copper Thickness',
    'PCB Copper Layers': 'PCB Copper Layers',
    'Solder Mask & Legend': 'Solder Mask & Legend',
    'Track/Spacings(mil)': 'Track/Spacings(mil)',
    'Via Drill/Finish': 'Via Drill/Finish',
    'PCB Thickness': 'PCB Thickness',
    'Quantity': 'Quantity',
    'Delivery Type': 'Delivery Type'
  };

  // Required fields (marked with *)
  const requiredFields = [
    'PCB Material',
    'PCB Finish',
    'Copper Thickness',
    'PCB Copper Layers',
    'Solder Mask & Legend',
    'Track/Spacings(mil)',
    'Via Drill/Finish',
    'PCB Thickness',
    'Delivery Type'
  ];

  const renderField = (fieldName, isRequired = false) => {
    const options = specOptions[fieldName] || [];
    const value = specifications[fieldName] || '';

    // Sanitize field name for use in HTML IDs (remove special characters)
    const sanitizedId = fieldName.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();

    // For text input fields (Quantity)
    if (fieldName === 'Quantity') {
      return (
        <div key={fieldName} className="spec-field">
          <label>{fieldLabels[fieldName] || fieldName}:</label>
          <input
            type="number"
            value={value}
            onChange={(e) => onChange(fieldName, e.target.value)}
            className="spec-input"
            placeholder="Enter quantity"
            min="1"
          />
        </div>
      );
    }

    // Use select dropdown for better browser compatibility
    return (
      <div key={fieldName} className="spec-field">
        <label>
          {fieldLabels[fieldName] || fieldName}
          {isRequired && <span className="required-asterisk">*</span>}:
        </label>
        <select
          value={value}
          onChange={(e) => onChange(fieldName, e.target.value)}
          className="spec-select"
          required={isRequired}
        >
          <option value="">Select {fieldLabels[fieldName] || fieldName}</option>
          {options.map((option, idx) => (
            <option key={idx} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
    );
  };

  // Field order as per image - arranged for 3-column grid
  // Grid fills row by row, so order is: row1-col1, row1-col2, row1-col3, row2-col1, row2-col2, row2-col3, etc.
  // Column 1: PCB Material, PCB Copper Layers, Via Drill/Finish, Delivery Type
  // Column 2: PCB Finish, Solder Mask & Legend, PCB Thickness
  // Column 3: Copper Thickness, Track/Spacings(mil), Quantity
  const fieldOrder = [
    'PCB Material',           // Row 1, Column 1
    'PCB Finish',             // Row 1, Column 2
    'Copper Thickness',       // Row 1, Column 3
    'PCB Copper Layers',      // Row 2, Column 1
    'Solder Mask & Legend',   // Row 2, Column 2
    'Track/Spacings(mil)',    // Row 2, Column 3
    'Via Drill/Finish',       // Row 3, Column 1
    'PCB Thickness',          // Row 3, Column 2
    'Quantity',               // Row 3, Column 3
    'Delivery Type'           // Row 4, Column 1
  ];

  return (
    <div className="pcb-specifications">
      <h2>PCB Specifications</h2>
      <div className="specifications-form">
        {fieldOrder.map(fieldName => 
          renderField(fieldName, requiredFields.includes(fieldName))
        )}
      </div>
      <button
        onClick={onCalculate}
        disabled={loading}
        className="calculate-button"
      >
        {loading ? 'Calculating...' : 'Calculate Rate Contract'}
      </button>
    </div>
  );
};

export default PCBSpecifications;


