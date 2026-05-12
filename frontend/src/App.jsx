import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import ExamplePrompts from './components/ExamplePrompts';
import SchemaViewer from './components/SchemaViewer';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [schema, setSchema] = useState(null);
  const [showSchema, setShowSchema] = useState(false);

  useEffect(() => {
    axios.get(`${API_BASE}/api/schema`)
      .then(res => setSchema(res.data))
      .catch(() => setSchema(null));
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE}/api/generate`, { prompt });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred. Check the backend logs.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) handleGenerate();
  };

  return (
    <div className="app-container">
      <header>
        <h1>QueryAI</h1>
        <p className="subtitle">Translate natural language to MySQL & MongoDB instantly</p>
      </header>

      <main>
        <section className="input-section glass-panel">
          <textarea
            placeholder="Describe what data you want... e.g. 'Find top 5 products with highest sales'"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <ExamplePrompts onSelect={setPrompt} />
          <div className="input-actions">
            <button className="schema-toggle-btn" onClick={() => setShowSchema(!showSchema)}>
              {showSchema ? 'Hide Schema' : 'View Schema'}
            </button>
            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={loading || !prompt.trim()}
            >
              {loading ? <span className="loader"></span> : '⚡ Generate Queries'}
            </button>
          </div>
        </section>

        {showSchema && schema && (
          <section className="schema-section glass-panel">
            <div className="schema-columns">
              <SchemaViewer schema={schema.mysql} title="MySQL Schema" icon="🐬" />
              <SchemaViewer schema={schema.mongodb} title="MongoDB Schema" icon="🍃" />
            </div>
          </section>
        )}

        {error && (
          <div className="error-message glass-panel">
            ⚠ {error}
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
                    options={{ readOnly: true, minimap: { enabled: false }, fontSize: 14 }}
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
                    options={{ readOnly: true, minimap: { enabled: false }, fontSize: 14 }}
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
