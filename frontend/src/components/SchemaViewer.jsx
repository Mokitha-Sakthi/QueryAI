import React from 'react';

export default function SchemaViewer({ schema, title, icon }) {
  if (!schema || Object.keys(schema).length === 0) {
    return (
      <div className="schema-viewer">
        <h3>{icon} {title}</h3>
        <p className="schema-empty">No schema available. Check your database connection.</p>
      </div>
    );
  }

  const error = schema._error;

  return (
    <div className="schema-viewer">
      <h3>{icon} {title}</h3>
      {error ? (
        <p className="schema-error">⚠ {error}</p>
      ) : (
        Object.entries(schema).map(([table, fields]) => (
          <div key={table} className="schema-table">
            <p className="schema-table-name">📋 {table}</p>
            <ul className="schema-fields">
              {fields.map((f, i) => (
                <li key={i}>
                  <span className="field-name">{f.field}</span>
                  <span className="field-type">{f.type}</span>
                  {f.key && <span className="field-key">{f.key}</span>}
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}
