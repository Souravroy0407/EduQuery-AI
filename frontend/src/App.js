import React from "react";
import Navbar from "./components/Navbar";
import QueryBox from "./components/QueryBox";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(180deg, #f5f9ff 0%, #dee8ff 100%)",
      }}
    >
      <Navbar />
      <div className="container py-5" style={{ maxWidth: "750px" }}>
        <QueryBox />
      </div>
      <ToastContainer position="top-right" theme="colored" />
    </div>
  );
}

export default App;
