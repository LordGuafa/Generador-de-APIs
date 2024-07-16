import axios from "axios";
import React from "react";
import "../styles/FileRead.css";

const FileRead = ({
  file,
  database,
  setDatabase,
  apiType,
  setApiType,
  setZipFileUrl,
  setZipFileName,
  setZipFileSize,
}) => {
  const Recargar = (event) => {
    event.preventDefault();
    window.location.reload();
  };

  const handleDatabaseChange = (event) => {
    setDatabase(event.target.value);
  };

  const handleApiTypeChange = (event) => {
    setApiType(event.target.value);
  };

  const subirarchivo = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("file", file);

    if (apiType === "Python" && database === "MongoDB") {
      alert("Python + MongoDB no disponeble en este momento");
    } else if (apiType === "Python" && database === "MySQL") {
      try {
        const response = await axios.post(
          "http://localhost:8000/generate_project",
          formData,
          {
            responseType: "blob",
          }
        );

        if (response.status === 200) {
          console.log("Archivo subido exitosamente");
          const zipBlob = new Blob([response.data], {
            type: "application/zip",
          });
          const zipUrl = URL.createObjectURL(zipBlob);

          // Guardar la URL y el nombre del archivo .zip
          setZipFileUrl(zipUrl);
          setZipFileName(file.name.replace(/\.[^/.]+$/, "") + ".zip");
          setZipFileSize(zipBlob.size);
        } else {
          console.error("Error al subir el archivo");
        }
      } catch (error) {
        console.error("Error de red:", error);
      }
    } else if (apiType === "Express" && database === "MySQL") {
      try {
        const response = await axios.post(
          "http://localhost:8000/GenerateProjectXpressSQL",
          formData,
          {
            responseType: "blob",
          }
        );

        if (response.status === 200) {
          console.log("Archivo subido exitosamente");
          const zipBlob = new Blob([response.data], {
            type: "application/zip",
          });
          const zipUrl = URL.createObjectURL(zipBlob);

          // Guardar la URL y el nombre del archivo .zip
          setZipFileUrl(zipUrl);
          setZipFileName(file.name.replace(/\.[^/.]+$/, "") + ".zip");
          setZipFileSize(zipBlob.size);
        } else {
          console.error("Error al subir el archivo");
        }
      } catch (error) {
        console.error("Error de red:", error);
      }
    } else if (apiType === "Express" && database === "MongoDB") {
      try {
        const response = await axios.post(
          "http://localhost:8000/GenerateProjectXpressMongoBD",
          formData,
          {
            responseType: "blob",
          }
        );

        if (response.status === 200) {
          console.log("Archivo subido exitosamente");
          const zipBlob = new Blob([response.data], {
            type: "application/zip",
          });
          const zipUrl = URL.createObjectURL(zipBlob);

          // Guardar la URL y el nombre del archivo .zip
          setZipFileUrl(zipUrl);
          setZipFileName(file.name.replace(/\.[^/.]+$/, "") + ".zip");
          setZipFileSize(zipBlob.size);
        } else {
          console.error("Error al subir el archivo");
        }
      } catch (error) {
        console.error("Error de red:", error);
      }
    }
  };

  return (
    <div className="container2">
      <h1>Has subido el siguiente documento</h1>
      <div className="upload-section">
        <div className="component-content">
          <div className="file-info">
            <img className="iconoxml" src="xmlicono.png" alt="Icon" />
            <div>
              <p>Nombre: {file.name}</p>
              <p>Tipo: {file.type}</p>
              <p>TamaÃ±o: {file.size}bytes</p>
            </div>
          </div>
          <div className="selectors">
            <p>Seleccione Base de datos:</p>
            <select value={database} onChange={handleDatabaseChange}>
              <option value="MySQL">MySQL</option>
              <option value="MongoDB">MongoDB</option>
            </select>
            <p>Seleccione Tipo de API:</p>
            <select value={apiType} onChange={handleApiTypeChange}>
              <option value="Python">Python</option>
              <option value="Express">Express</option>
            </select>
          </div>
          <button className="subirarchivoapi" onClick={subirarchivo}>
            Subir archivo
          </button>
        </div>
      </div>
      <button className="atras" onClick={Recargar}>
        Regresar
      </button>
    </div>
  );
};

export default FileRead;
