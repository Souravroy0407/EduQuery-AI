import React from "react";
import Navbar from "./components/Navbar";
import PDFUpload from "./components/PDFUpload";
import QueryBox from "./components/QueryBox";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <>
      <Navbar />
      <div className="container mt-5">
        <PDFUpload />
        <QueryBox />
      </div>
      <ToastContainer position="top-right" autoClose={3000} />
    </>
  );
}

export default App;
