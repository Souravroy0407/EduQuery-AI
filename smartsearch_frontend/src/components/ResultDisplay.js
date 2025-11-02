import React from "react";
import ReactMarkdown from "react-markdown";

function ResultDisplay({ result }) {
  if (!result?.answer) return null;

  return (
    <div className="mt-4 p-4 bg-light rounded shadow-sm border">
      <h5 className="fw-bold mb-3">💡 Answer</h5>

      <div
        className="fs-6"
        style={{
          whiteSpace: "pre-wrap",
          lineHeight: "1.7",
          textAlign: "justify",
        }}
      >
        <ReactMarkdown>{result.answer}</ReactMarkdown>
      </div>
    </div>
  );
}

export default ResultDisplay;
