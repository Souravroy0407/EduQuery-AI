import React, { useState } from "react";
import api from "../api";
import { toast } from "react-toastify";

function PDFUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      toast.warn("Please select a PDF first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const res = await api.post("upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success("✅ PDF uploaded successfully!");
      console.log(res.data);
      setFile(null);
      if (onUploadComplete) onUploadComplete(); // auto close modal
    } catch (error) {
      toast.error("❌ Upload failed!");
      console.error(error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="text-center">
      <input
        type="file"
        className="form-control mb-3"
        accept=".pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        onClick={handleUpload}
        className="btn btn-primary"
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}

export default PDFUpload;
