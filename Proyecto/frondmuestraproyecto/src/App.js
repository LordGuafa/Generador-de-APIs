import React, { useState } from 'react';
import './styles/style.css';
import axios from './api/axios';
function App() {
  
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  };

  const handleFileDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    setFile(droppedFile);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleFileUpload = async () => {
    if (!file) {
      alert('Por favor, selecciona un archivo primero.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('generate_project', formData, {
        
      });

      if (response.status === 200) {
        console.log('Archivo subido exitosamente');
      } else {
        console.error('Error al subir el archivo');
      }
    } catch (error) {
      console.error('Error de red:', error);
    }
  };

  return (
    <div className="container">
      <h1>Editar Archivo XML Gratis</h1>
      <div className="upload-section">
        <div
          className="upload-box"
          onDrop={handleFileDrop}
          onDragOver={handleDragOver}
        >
          <input
            type="file"
            id="fileInput"
            accept=".xml"
            onChange={handleFileChange}
          />
          <label htmlFor="fileInput">Arrastra y suelta el documento aquí para subirlo</label>
          <button onClick={() => document.getElementById('fileInput').click()}>
            Seleccionar desde el dispositivo
          </button>
        </div>
        <p>El xml debe cumplir con el siguiente archivo<a href="/modelorelacional.xsd" download> .XSD</a></p>
        <p>Puede validar su .XML en: <a href="https://www.freeformatter.com/xml-validator-xsd.html" target="_blank" rel="noopener noreferrer">freeformatter</a></p>
      </div>
      {file && (
        <div className="file-info">
          <h2>Archivo subido:</h2>
          <p>Nombre: {file.name}</p>
          <p>Tamaño: {file.size} bytes</p>
          <button onClick={handleFileUpload}>Subir Archivo</button>
        </div>
      )}
    </div>
  );
}

export default App;