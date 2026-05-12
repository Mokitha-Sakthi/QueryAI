import React from 'react';

const EXAMPLE_PROMPTS = [
  "Find the top 5 products with the highest sales revenue",
  "Get all users who signed up in the last 7 days",
  "Show orders that are pending and older than 3 days",
  "Count the number of users by country",
];

export default function ExamplePrompts({ onSelect }) {
  return (
    <div className="example-prompts">
      <p className="examples-label">Try an example:</p>
      <div className="examples-list">
        {EXAMPLE_PROMPTS.map((p, i) => (
          <button key={i} className="example-chip" onClick={() => onSelect(p)}>
            {p}
          </button>
        ))}
      </div>
    </div>
  );
}
