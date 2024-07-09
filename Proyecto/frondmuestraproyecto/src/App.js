import React from 'react';
import './styles/style.css';

function App() {
  return (
    <div className="container">
      <h1>Editar Archivo XML Gratis</h1>
      <div className="upload-section">
        <div className="upload-box">
          <input type="file" id="fileInput" accept=".xml" />
          <label htmlFor="fileInput">Arrastra y suelta el documento aquí para subirlo</label>
          <button>Seleccionar desde el dispositivo</button>
        </div>
        <p>El xml debe cumplir con el siguiente archivo<a href="/modelorelacional.xsd" download> .XSD</a></p>
        <p>Puede validar su .XML en: <a href="https://www.freeformatter.com/xml-validator-xsd.html" target="_blank" rel="noopener noreferrer">freeformatter</a></p>
      </div>
    </div>
  );
}

export default App;
