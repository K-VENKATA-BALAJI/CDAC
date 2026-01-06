import React from 'react';
import './PCBRates.css';

const PCBRates = ({ vendors }) => {
  // Always show table structure, even if empty
  const displayVendors = vendors && vendors.length > 0 ? vendors : [];
  const emptyRows = vendors && vendors.length > 0 ? 0 : 4; // Show 4 empty rows when no data

  return (
    <div className="pcb-rates">
      <h2>PCB Rates</h2>
      <div className="rates-table-container">
        <table className="rates-table">
          <thead>
            <tr>
              <th>s.No</th>
              <th>Vendor Name</th>
              <th>Rate</th>
              <th>Rank</th>
            </tr>
          </thead>
          <tbody>
            {displayVendors.map((vendor, index) => (
              <tr key={index}>
                <td>{vendor.sno || index + 1}</td>
                <td>{vendor.vendor_name}</td>
                <td>${vendor.rate.toFixed(2)}</td>
                <td>L{vendor.rank || index + 1}</td>
              </tr>
            ))}
            {emptyRows > 0 && Array.from({ length: emptyRows }).map((_, index) => (
              <tr key={`empty-${index}`} className="empty-row">
                <td>{displayVendors.length + index + 1}</td>
                <td></td>
                <td></td>
                <td>L{displayVendors.length + index + 1}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PCBRates;


