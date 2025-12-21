import React, { useState } from 'react';
import './App.css';
import PCBCalculator from './components/PCBCalculator';

function App() {
  const [loadedData, setLoadedData] = useState(null);

  const handleNewFile = () => {
    setLoadedData(null);
  };

  const handleLoadFile = (data) => {
    setLoadedData(data);
  };

  return (
    <div className="App">
      <PCBCalculator 
        loadedData={loadedData}
        onNewFile={handleNewFile}
        onLoadFile={handleLoadFile}
      />
    </div>
  );
}

export default App;


