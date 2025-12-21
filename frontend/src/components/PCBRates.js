import React from 'react';
import './PCBRates.css';

const PCBRates = ({ vendors }) => {
  if (!vendors || vendors.length === 0) {
    return (
      <div className="pcb-rates">
        <h2>PCB Rates</h2>
        <div className="empty-state">
          <p>Click "Calculate Rate Contract" to see vendor rates</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pcb-rates">
      <h2>PCB Rates</h2>
      <div className="rates-table-container">
        <table className="rates-table">
          <thead>
            <tr>
              <th>S.NO</th>
              <th>Vendor Name</th>
              <th>Rate</th>
              <th>Rank</th>
            </tr>
          </thead>
          <tbody>
            {vendors.map((vendor, index) => (
              <tr key={index}>
                <td>{vendor.sno || index + 1}</td>
                <td>{vendor.vendor_name}</td>
                <td>${vendor.rate.toFixed(2)}</td>
                <td>{vendor.rank}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PCBRates;


