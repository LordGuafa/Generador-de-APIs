import axios from "axios";
import React from "react";
import "../styles/FileDownload.css";
const FileDownload = ({ zipFileUrl, zipFileName, zipFileSize, file }) => {
  const Recargar = (event) => {
    event.preventDefault();
    window.location.reload();
  };
  const descargarArchivo = async () => {
    const a = document.createElement("a");
    a.href = zipFileUrl;
    a.download = zipFileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    await axios.get("http://localhost:8000/eliminar/" + file.name);
    setTimeout(() => {
      window.location.reload();
    }, 1000); // Espera 1 segundo antes de recargar la página
  };

  return (
    <div className="container3">
      <h1>Tu api</h1>
      <div className="upload-section">
        <div className="component-content">
          <div className="file-info">
            <img className="zipicono" src="zipicono.png" alt="Icon" />
            <div>
              <p>Nombre: {zipFileName}</p>
              <p>Tipo: ZIP</p>
              <p>Tamaño: {zipFileSize}bytes</p>
            </div>
          </div>
          <button className="Descargarproyecto" onClick={descargarArchivo}>
            Descargar proyecto
          </button>
        </div>
      </div>
      <button className="atras" onClick={Recargar}>
        Regresar
      </button>
    </div>
  );
};

export default FileDownload;
