import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github-dark.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "./ResultDisplay.css"; // optional custom styles

function ResultDisplay({ result }) {
  if (!result?.answer) return null;

  return (
    <div className="mt-4 p-4 rounded-4 shadow-lg bg-white border-0 animate__animated animate__fadeIn">
      <h5 className="fw-bold text-gradient mb-3">💡 Answer</h5>
      <div className="markdown-body fs-5 lh-base">
        <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
          {result.answer}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default ResultDisplay;
