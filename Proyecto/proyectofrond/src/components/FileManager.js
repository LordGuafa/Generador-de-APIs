// src/components/FileManager.js
import React, { useState } from "react";
import FileDownload from "./FileDownload";
import FileRead from "./FileRead";
import FileUpload from "./FileUpload";

const FileManager = () => {
  const [file, setFile] = useState(null);
  const [database, setDatabase] = useState("MySQL");
  const [apiType, setApiType] = useState("Python");
  const [zipFileUrl, setZipFileUrl] = useState(null);
  const [zipFileName, setZipFileName] = useState("");
  const [zipFileSize, setZipFileSize] = useState(0);

  return (
    <div>
      {!file ? (
        <FileUpload setFile={setFile} />
      ) : !zipFileUrl ? (
        <FileRead
          file={file}
          database={database}
          setDatabase={setDatabase}
          apiType={apiType}
          setApiType={setApiType}
          setZipFileUrl={setZipFileUrl}
          setZipFileName={setZipFileName}
          setZipFileSize={setZipFileSize}
        />
      ) : (
        <FileDownload
          zipFileUrl={zipFileUrl}
          zipFileName={zipFileName}
          zipFileSize={zipFileSize}
          file={file}
        />
      )}
    </div>
  );
};

export default FileManager;
