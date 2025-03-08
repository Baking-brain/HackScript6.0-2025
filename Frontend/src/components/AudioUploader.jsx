// src/components/AudioUploader.jsx
import React, { useState } from "react";
import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;

const AudioUploader = ({ onUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      handleFileUpload(file);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      handleFileUpload(file);
    }
  };

  const handleFileUpload = (file) => {
    setUploadedFile(file);
    onUpload(file);
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
    onUpload(null);
  };

  const handleAnalyse = async () => {
    const formData = new FormData();
    formData.append("audio_file", uploadedFile);

    await axios
      .post(apiUrl + "/api/upload_file", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error.response.data);
      });
  };

  return (
    <div className="audio-uploader">
      {!uploadedFile ? (
        <form
          className={`upload-form ${dragActive ? "active" : ""}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="upload-file"
            accept="audio/*"
            onChange={handleChange}
            className="input-file"
          />
          <label htmlFor="upload-file" className="upload-label">
            <div className="upload-icon">
              <i className="fas fa-cloud-upload-alt"></i>
            </div>
            <div className="upload-text">
              <p>Drag and drop audio file here or click to upload</p>
              <p className="upload-hint">Supports MP3, WAV, M4A formats</p>
            </div>
          </label>
        </form>
      ) : (
        <div className="uploaded-file-container">
          <div className="uploaded-file-details">
            <div className="uploaded-file-icon">
              <i className="fas fa-file-audio"></i>
            </div>
            <div className="uploaded-file-info">
              <h3 className="uploaded-file-name">{uploadedFile.name}</h3>
              <p className="uploaded-file-meta">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB •
                {uploadedFile.type.split("/")[1].toUpperCase()}
              </p>
            </div>
            <div className="uploaded-file-status">
              <span className="status-badge success">Ready for Analysis</span>
            </div>
          </div>
          <div className="uploaded-file-actions">
            <button
              className="remove-file-btn"
              onClick={handleRemoveFile}
              type="button"
            >
              <i className="fas fa-times"></i> Remove
            </button>
            <button
              className="analyze-btn"
              type="button"
              onClick={handleAnalyse}
            >
              <i className="fas fa-chart-line"></i> Start Analysis
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AudioUploader;
