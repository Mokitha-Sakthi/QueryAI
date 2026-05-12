import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    setResults(null);
    
    try {
      const response = await axios.post('http://localhost:8000/api/generate', { prompt });
      setResults(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An error occurred while generating queries. Check console and backend logs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>QueryBridge AI</h1>
        <p className="subtitle">Translate Natural Language to MySQL & MongoDB</p>
      </header>

      <main>
        <section className="input-section glass-panel">
          <textarea 
            placeholder="E.g., Find the top 5 products with the highest sales in the last month..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button 
            className="generate-btn" 
            onClick={handleGenerate} 
            disabled={loading || !prompt.trim()}
          >
            {loading ? <span className="loader"></span> : 'Generate Queries'}
          </button>
        </section>

        {error && (
          <div className="error-message glass-panel" style={{ padding: '1rem', color: '#ef4444', marginTop: '1rem' }}>
            {error}
          </div>
        )}

        {results && (
          <>
            <section className="results-section">
              <div className="code-container glass-panel">
                <h2>🐬 MySQL Query</h2>
                <div className="editor-wrapper">
                  <Editor
                    height="100%"
                    language="sql"
                    theme="vs-dark"
                    value={results.sql}
                    options={{ readOnly: true, minimap: { enabled: false } }}
                  />
                </div>
              </div>

              <div className="code-container glass-panel">
                <h2>🍃 MongoDB Pipeline</h2>
                <div className="editor-wrapper">
                  <Editor
                    height="100%"
                    language="json"
                    theme="vs-dark"
                    value={results.mongodb}
                    options={{ readOnly: true, minimap: { enabled: false } }}
                  />
                </div>
              </div>
            </section>

            {results.explanation && (
              <section className="explanation-section glass-panel">
                <h3>💡 Explanation</h3>
                <p>{results.explanation}</p>
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
