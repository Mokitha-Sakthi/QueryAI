import React, { useState, useEffect, useCallback } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import SchemaViewer from './components/SchemaViewer';
import './App.css';

const API_BASE = 'http://localhost:8000';

// All available databases (one selector, pick one)
const DB_OPTIONS = {
  queryai_shop: { type: 'mysql', label: 'Shop (E-commerce)', icon: '🐬', detail: 'customers · products · orders' },
  queryai_hr: { type: 'mysql', label: 'HR System', icon: '🐬', detail: 'departments · employees · leave_requests' },
  queryai_blog: { type: 'mongodb', label: 'Blog Platform', icon: '🍃', detail: 'users · posts · comments' },
  queryai_iot: { type: 'mongodb', label: 'IoT Sensors', icon: '🍃', detail: 'devices · readings · alerts' },
};

// Example prompts per database
const EXAMPLE_PROMPTS = {
  queryai_shop: [
    "Show all VIP customers",
    "Find the top 3 most expensive products",
    "Show all delivered orders with total price above 100",
    "Count orders by status",
    "List all products in the Electronics category",
  ],
  queryai_hr: [
    "Show all active employees with their department name",
    "Find employees earning more than 80000",
    "List all pending leave requests",
    "Show total salary budget per department",
    "Find employees hired after 2021",
  ],
  queryai_blog: [
    "Show all published posts with more than 300 likes",
    "Count posts by author",
    "Find all admin or editor users",
    "Show the most viewed posts",
    "Get all comments with more than 5 likes",
  ],
  queryai_iot: [
    "Show all active devices",
    "Find all unresolved alerts",
    "List all temperature sensor readings",
    "Show devices registered after 2023",
    "Find all critical alerts",
  ],
};

function App() {
  const [selectedDb, setSelectedDb] = useState('queryai_shop');
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [schema, setSchema] = useState(null);
  const [schemaLoading, setSchemaLoading] = useState(false);
  const [schemaError, setSchemaError] = useState(null);
  const [showSchema, setShowSchema] = useState(false);

  const dbInfo = DB_OPTIONS[selectedDb];
  const dbType = dbInfo.type;

  const fetchSchema = useCallback(async (dbName) => {
    setSchemaLoading(true);
    setSchemaError(null);
    setSchema(null);
    try {
      const res = await axios.get(`${API_BASE}/api/schema`, {
        params: { db_name: dbName }
      });
      setSchema(res.data);
    } catch (e) {
      setSchemaError('Could not load schema. Is the backend running?');
    } finally {
      setSchemaLoading(false);
    }
  }, []);

  // Fetch schema whenever db selection changes
  useEffect(() => {
    fetchSchema(selectedDb);
  }, [selectedDb, fetchSchema]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE}/api/generate`, {
        prompt,
        db_name: selectedDb,
      });
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

  const handleSelectDb = (key) => {
    setSelectedDb(key);
    setResults(null);
    setError(null);
  };

  const examples = EXAMPLE_PROMPTS[selectedDb] || [];

  // Determine result heading & language for the editor
  const isMySQL = dbType === 'mysql';
  const resultHeading = isMySQL ? '🐬 MySQL Query' : '🍃 MongoDB Aggregation Pipeline';
  const resultBadgeClass = isMySQL ? 'mysql-badge' : 'mongo-badge';
  const editorLanguage = isMySQL ? 'sql' : 'javascript';

  // Get the query string from results
  const getQueryString = () => {
    if (!results) return '';
    // The backend returns { query, explanation }
    const q = results.query;
    if (typeof q === 'string') return q;
    return JSON.stringify(q, null, 2);
  };

  return (
    <div className="app-container">
      <header>
        <h1>QueryAI</h1>
        <p className="subtitle">Translate natural language to database queries instantly</p>
      </header>

      {/* ── Single Database Selector ────────────────────────────── */}
      <section className="db-selector-bar glass-panel">
        <div className="db-selector-group" style={{ flex: 'unset', width: '100%' }}>
          <label className="db-selector-label">
            <span className="db-icon">🗄️</span> Select Database
          </label>
          <div className="db-pills">
            {Object.entries(DB_OPTIONS).map(([key, info]) => (
              <button
                key={key}
                className={`db-pill ${selectedDb === key ? `active ${info.type === 'mysql' ? 'mysql-active' : 'mongo-active'}` : ''}`}
                onClick={() => handleSelectDb(key)}
              >
                <span className="pill-label">{info.icon} {info.label}</span>
                <span className="pill-sub">{info.detail}</span>
                <span className="pill-type-tag" data-type={info.type}>
                  {info.type === 'mysql' ? 'MySQL' : 'MongoDB'}
                </span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* ── Main Input ──────────────────────────────────────────── */}
      <section className="input-section glass-panel">
        <textarea
          placeholder={`Describe what data you want from ${dbInfo.label}… e.g. '${examples[0] || 'Find all records'}' (Ctrl+Enter to generate)`}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        {/* Example Chips */}
        <div className="example-prompts">
          <p className="examples-label">Try an example:</p>
          <div className="examples-list">
            {examples.map((p, i) => (
              <button key={i} className="example-chip" onClick={() => setPrompt(p)}>
                {p}
              </button>
            ))}
          </div>
        </div>

        <div className="input-actions">
          <button className="schema-toggle-btn" onClick={() => setShowSchema(s => !s)}>
            {showSchema ? '▲ Hide Schema' : '▼ View Schema'}
          </button>
          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
          >
            {loading ? <span className="loader" /> : `⚡ Generate ${isMySQL ? 'SQL' : 'MongoDB'} Query`}
          </button>
        </div>
      </section>

      {/* ── Schema Panel ────────────────────────────────────────── */}
      {showSchema && (
        <section className="schema-section glass-panel">
          {schemaLoading && <p className="schema-loading">Loading schema…</p>}
          {schemaError && <p className="schema-error">⚠ {schemaError}</p>}
          {schema && !schemaLoading && (
            <SchemaViewer
              schema={schema.schema}
              title={`${dbInfo.icon} ${isMySQL ? 'MySQL' : 'MongoDB'} — ${dbInfo.label}`}
              icon={dbInfo.icon}
              dbType={dbType}
            />
          )}
        </section>
      )}

      {/* ── Error ───────────────────────────────────────────────── */}
      {error && (
        <div className="error-message glass-panel">
          ⚠ {error}
        </div>
      )}

      {/* ── Results (single query) ──────────────────────────────── */}
      {results && (
        <>
          <section className="results-section single-result">
            <div className="code-container glass-panel">
              <h2>
                {resultHeading}
                <span className={`result-db-badge ${resultBadgeClass}`}>{selectedDb}</span>
              </h2>
              <div className="editor-wrapper">
                <Editor
                  height="100%"
                  language={editorLanguage}
                  theme="vs-dark"
                  value={getQueryString()}
                  options={{ readOnly: true, minimap: { enabled: false }, fontSize: 14, wordWrap: 'on' }}
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
    </div>
  );
}

export default App;
