import React, { useState } from "react";
import api from "../api";
import { toast } from "react-toastify";
import ResultDisplay from "./ResultDisplay";

function QueryBox() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await api.post("query/", { question: query });
      setResult(res.data);
      toast.success("✅ Answer generated!");
    } catch (error) {
      toast.error("⚠️ Error fetching answer!");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="card p-4 mt-5 border-0 shadow-sm rounded-4"
      style={{ background: "#ffffff" }}
    >
      <h5 className="fw-bold mb-3 text-success">🤖 Ask EduQuery AI</h5>
      <textarea
        className="form-control mb-3"
        rows="3"
        placeholder="Ask something from your uploaded notes..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      ></textarea>
      <button
        onClick={handleAsk}
        className="btn btn-success w-100 rounded-pill"
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default QueryBox;
