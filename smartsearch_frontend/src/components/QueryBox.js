import React, { useState } from "react";
import api from "../api";
import { toast } from "react-toastify";
import ResultDisplay from "./ResultDisplay";

function QueryBox() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) {
      toast.warn("⚠️ Please enter a question!");
      return;
    }

    setLoading(true);
    try {
      const res = await api.post("query/", { question });
      setResult(res.data);
      toast.success("💡 Answer generated!");
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.error || "❌ Query failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card p-4 shadow-sm mt-4">
      <h5>🤖 Ask EduQuery AI</h5>
      <textarea
        className="form-control mt-2"
        rows="3"
        placeholder="Ask something from your uploaded notes..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      ></textarea>
      <button
        onClick={handleAsk}
        className="btn btn-success mt-3"
        disabled={loading}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default QueryBox;
