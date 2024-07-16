import React, { useRef } from 'react';
import '../styles/FileUpload.css';

const FileUpload = ({ setFile }) => {
    const fileInputRef = useRef(null);

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
    
    return (
        <div className="container">
            <h1>Editar Archivo XML Gratis</h1>
            <div className="upload-section">
                <div 
                    className="upload-box"
                    onDrop={handleFileDrop} 
                    onDragOver={handleDragOver}
                >
                    <label htmlFor="file-upload">Arrastra y suelta el documento aquí para subirlo</label>
                    <input 
                        type="file" 
                        id="file-upload" 
                        ref={fileInputRef}
                        onChange={handleFileChange}
                    />
                    <button onClick={() => document.getElementById('file-upload').click()}>Seleccionar desde el dispositivo</button>
                </div>
                <p>El xml debe cumplir con el siguiente archivo<a href="/modelorelacional.xsd" download> .XSD</a></p>
                <p>Puede validar su .XML en: <a href="https://www.freeformatter.com/xml-validator-xsd.html" target="_blank" rel="noopener noreferrer">freeformatter</a></p>
            </div>
        </div>
    );
}

export default FileUpload;