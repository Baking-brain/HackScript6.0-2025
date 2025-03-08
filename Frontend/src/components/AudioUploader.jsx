// src/components/AudioUploader.jsx
import React, { useState } from 'react';

const AudioUploader = ({ onUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };
  
  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };
  
  return (
    <div className="audio-uploader">
      <form 
        className={`upload-form ${dragActive ? 'active' : ''}`} 
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
    </div>
  );
};

export default AudioUploader;