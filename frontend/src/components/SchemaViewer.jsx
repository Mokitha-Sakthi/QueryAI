import React, { useState } from 'react';

export default function SchemaViewer({ schema, title, icon, dbType }) {
  const [expanded, setExpanded] = useState({});

  const toggle = (name) => setExpanded(prev => ({ ...prev, [name]: !prev[name] }));

  if (!schema) {
    return (
      <div className="schema-viewer">
        <h3><span className="schema-icon">{icon}</span> {title}</h3>
        <p className="schema-empty">Loading…</p>
      </div>
    );
  }

  if (schema._error) {
    return (
      <div className="schema-viewer">
        <h3><span className="schema-icon">{icon}</span> {title}</h3>
        <div className="schema-error-box">
          <span className="schema-error-icon">⚠</span>
          <p className="schema-error">{schema._error}</p>
        </div>
      </div>
    );
  }

  const entries = Object.entries(schema);
  if (entries.length === 0) {
    return (
      <div className="schema-viewer">
        <h3><span className="schema-icon">{icon}</span> {title}</h3>
        <p className="schema-empty">No tables/collections found in this database.</p>
      </div>
    );
  }

  const tableLabel = dbType === 'mongodb' ? 'collection' : 'table';

  return (
    <div className="schema-viewer">
      <h3>
        <span className="schema-icon">{icon}</span> {title}
        <span className="schema-count">{entries.length} {tableLabel}{entries.length !== 1 ? 's' : ''}</span>
      </h3>
      <div className="schema-tables-list">
        {entries.map(([name, fields]) => (
          <div key={name} className="schema-table">
            <button className="schema-table-header" onClick={() => toggle(name)}>
              <span className="schema-table-icon">{dbType === 'mongodb' ? '📂' : '📋'}</span>
              <span className="schema-table-name">{name}</span>
              <span className="schema-field-count">{fields.length} field{fields.length !== 1 ? 's' : ''}</span>
              <span className="schema-chevron">{expanded[name] ? '▲' : '▼'}</span>
            </button>
            {expanded[name] && (
              <ul className="schema-fields">
                {fields.map((f, i) => (
                  <li key={i} className="schema-field-row">
                    <span className="field-name">{f.field}</span>
                    <span className="field-type">{f.type}</span>
                    {f.key && <span className="field-key">{f.key}</span>}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
