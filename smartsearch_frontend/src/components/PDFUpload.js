import React, { useState } from "react";
import api from "../api";
import { toast } from "react-toastify";

function PDFUpload() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      toast.warn("⚠️ Please select a PDF first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success("✅ PDF uploaded successfully!");
      console.log(res.data);
    } catch (error) {
      toast.error("❌ Upload failed!");
      console.error(error);
    }
  };

  return (
    <div className="card p-4 shadow-sm">
      <h5>📚 Upload Study PDF</h5>
      <input
        type="file"
        className="form-control mt-2"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} className="btn btn-primary mt-3">
        Upload
      </button>
    </div>
  );
}

export default PDFUpload;
