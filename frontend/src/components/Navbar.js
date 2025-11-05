import React, { useState } from "react";
import { Navbar, Container, Button, Modal } from "react-bootstrap";
import PDFUpload from "./PDFUpload";

function NavBar() {
  const [showUpload, setShowUpload] = useState(false);

  const handleOpen = () => setShowUpload(true);
  const handleClose = () => setShowUpload(false);

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" className="shadow-sm">
        <Container className="d-flex justify-content-between">
          <Navbar.Brand className="fw-bold text-info">
            🎓 EduQuery AI
          </Navbar.Brand>
          <Button variant="info" className="text-dark fw-semibold" onClick={handleOpen}>
            📤 Upload PDF
          </Button>
        </Container>
      </Navbar>

      {/* Upload Modal */}
      <Modal show={showUpload} onHide={handleClose} centered backdrop="static" keyboard={false}>
        <Modal.Header closeButton>
          <Modal.Title>📚 Upload Study PDF</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <PDFUpload onUploadComplete={handleClose} />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default NavBar;
