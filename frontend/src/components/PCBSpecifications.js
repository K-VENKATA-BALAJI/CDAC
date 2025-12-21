import React from 'react';
import './PCBSpecifications.css';

const PCBSpecifications = ({ specifications, specOptions, onChange, onCalculate, loading }) => {
  const fieldLabels = {
    'Num of Layers': 'Num of Layers',
    'Material': 'Material',
    'Surface Finish': 'Surface Finish',
    'Track / Spacing': 'Track / Spacing',
    'Via Filling': 'Via Filling',
    'Via Hole/Pad': 'Via Hole/Pad',
    'Thickness': 'Thickness',
    'Copper Thickness': 'Copper Thickness',
    'Size': 'Size',
    'Single Ended Impedance': 'Single Ended Impedance',
    'Colour': 'Colour',
    'Differential Impedance': 'Differential Impedance'
  };

  const renderField = (fieldName) => {
    const options = specOptions[fieldName] || [];
    const value = specifications[fieldName] || '';

    return (
      <div key={fieldName} className="spec-field">
        <label>{fieldLabels[fieldName] || fieldName}:</label>
        <select
          value={value}
          onChange={(e) => onChange(fieldName, e.target.value)}
          className="spec-select"
        >
          {options.map((option, idx) => (
            <option key={idx} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
    );
  };

  // Organize fields into 3 columns as per image
  const leftColumnFields = ['Num of Layers', 'Track / Spacing', 'Thickness', 'Single Ended Impedance', 'Differential Impedance'];
  const middleColumnFields = ['Material', 'Via Filling', 'Copper Thickness', 'Colour'];
  const rightColumnFields = ['Surface Finish', 'Via Hole/Pad', 'Size'];

  return (
    <div className="pcb-specifications">
      <h2>PCB Specifications</h2>
      <div className="specifications-form">
        <div className="spec-column">
          {leftColumnFields.map(renderField)}
        </div>
        <div className="spec-column">
          {middleColumnFields.map(renderField)}
        </div>
        <div className="spec-column">
          {rightColumnFields.map(renderField)}
        </div>
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


