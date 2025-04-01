import React, { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleSubmit = async () => {
    setLoading(true);
    const res = await fetch(process.env.REACT_APP_BACKEND_URL + '/api/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setResult(data.result);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', textAlign: 'center' }}>
      <h1>Manthan AI</h1>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your question"
        style={{ width: '100%', padding: '10px' }}
      />
      <button onClick={handleSubmit} disabled={loading} style={{ marginTop: '10px' }}>
        {loading ? 'Researching...' : 'Start Deep Research'}
      </button>
      <div style={{ marginTop: '20px', textAlign: 'left' }}>
        <pre>{result}</pre>
      </div>
    </div>
  );
}

export default App;
