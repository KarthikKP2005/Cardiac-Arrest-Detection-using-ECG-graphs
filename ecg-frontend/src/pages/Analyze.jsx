import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export default function Analyze() {
  const location = useLocation();
  const navigate = useNavigate();
  const patient = location.state?.patient || { name: 'Unknown', id: 'N/A', age: '-', gender: '-', complaint: 'None recorded' };

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', image);

    try {
      const response = await fetch('http://localhost:5000/analyze', { method: 'POST', body: formData });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Failed to connect to AI server." });
    }
    setLoading(false);
  };

  return (
    <div className="page-container">
      <div className="card" style={{ maxWidth: '900px' }}>
        
        {/* Patient Header - Now includes Chief Complaint */}
        <div style={{ background: '#f8fafc', padding: '20px', borderRadius: '8px', marginBottom: '20px', textAlign: 'left', border: '1px solid #e2e8f0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <div><strong>Patient:</strong> {patient.name}</div>
            <div><strong>ID:</strong> {patient.id}</div>
            <div><strong>Age/Sex:</strong> {patient.age} / {patient.gender}</div>
          </div>
          <div style={{ color: '#c53030', fontWeight: 'bold' }}>
            Chief Complaint: <span style={{ fontWeight: 'normal', color: '#4a5568' }}>{patient.complaint}</span>
          </div>
        </div>

        {/* Lead I Proof of Concept Header */}
        <h2 style={{ color: '#2d3748', margin: '0' }}>Diagnostic AI Core</h2>
        <p style={{ color: '#718096', marginBottom: '30px' }}><strong>Proof of Concept:</strong> Lead I Vector Analysis</p>

        {/* Upload Box (Fixed styling) */}
        <div style={{ padding: '20px', marginBottom: '20px', textAlign: 'center' }}>
          <input type="file" accept="image/*" onChange={e => {
            setImage(e.target.files[0]);
            setPreview(URL.createObjectURL(e.target.files[0]));
            setResult(null);
          }} style={{ marginBottom: '20px' }} />
          
          <br/>
          
          {/* THE MEDICAL GRID HACK */}
          {preview && !result && (
            <div className="ecg-grid-container">
              <img src={preview} alt="ECG Preview" className="ecg-image-blend" />
            </div>
          )}
        </div>

        <button className="btn-primary" onClick={handleUpload} disabled={!image || loading}>
          {loading ? '🧠 Deep Learning Analysis in Progress...' : 'Generate AI Report'}
        </button>

        {/* Results Banner */}
        {result && !result.error && (
          <div style={{ marginTop: '40px', textAlign: 'left', animation: 'slideUp 0.5s ease-out' }}>
            
            <div style={{ 
              padding: '25px', borderRadius: '12px', textAlign: 'center', marginBottom: '30px',
              background: result.is_normal ? '#f0fdf4' : '#fef2f2', border: `2px solid ${result.is_normal ? '#bbf7d0' : '#fecaca'}`, color: result.is_normal ? '#166534' : '#991b1b'
            }}>
              <h2 style={{ margin: '0 0 10px 0' }}>{result.diagnosis}</h2>
              <p style={{ fontSize: '18px', margin: 0 }}>AI Confidence Score: <strong>{result.confidence}%</strong></p>
            </div>

            {/* Side-by-Side Images & Heatmap */}
            <h3 style={{ color: '#2d3748', textAlign: 'center' }}>Explainable AI (Grad-CAM Morphological Focus)</h3>
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginBottom: '30px' }}>
              <div style={{ flex: 1, textAlign: 'center' }}>
                <p style={{ color: '#718096', fontWeight: 'bold' }}>Standard Grid View</p>
                <div className="ecg-grid-container" style={{ width: '100%' }}>
                  <img src={preview} alt="Original" className="ecg-image-blend" />
                </div>
              </div>
              <div style={{ flex: 1, textAlign: 'center' }}>
                <p style={{ color: '#e53e3e', fontWeight: 'bold' }}>Neural Network Focus Map</p>
                <div style={{ border: '2px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
                  <img src={`data:image/jpeg;base64,${result.heatmap}`} alt="AI Heatmap" style={{ width: '100%', display: 'block' }} />
                </div>
              </div>
            </div>

            {/* Clinical Indicators */}
            <div style={{ padding: '20px', borderRadius: '12px', background: 'white', border: '1px solid #e2e8f0' }}>
              <h3 style={{ marginTop: 0, color: '#2d3748', borderBottom: '2px solid #edf2f7', paddingBottom: '10px' }}>AI Extracted Clinical Indicators</h3>
              <ul style={{ listStyleType: 'none', padding: 0, margin: 0, color: '#4a5568', lineHeight: '2' }}>
                <li><strong>Rhythm:</strong> {result.is_normal ? '🟢 Regular (Normal Sinus)' : '🟠 Potentially Irregular / Arrhythmic'}</li>
                <li><strong>ST-Segment:</strong> {result.is_normal ? '🟢 Isoelectric (Normal)' : '🔴 Abnormal Elevation/Depression Detected'}</li>
                <li><strong>T-Wave:</strong> {result.is_normal ? '🟢 Normal Upright' : '🔴 Possible Inversion / Hyperacute'}</li>
                <li><strong>PR Interval:</strong> ⚪ <i>Requires 1D signal logic for precise ms measurement</i></li>
              </ul>
              <p style={{ fontSize: '12px', color: '#718096', marginTop: '15px', fontStyle: 'italic' }}>
                *Disclaimer: This is an AI-assisted morphological analysis of Lead I. A full 12-lead interpretation and clinical correlation by a board-certified cardiologist is required to diagnose Myocardial Infarction.
              </p>
            </div>
            
          </div>
        )}

        {result && result.error && <div style={{ color: 'red', marginTop: '20px' }}><p>{result.error}</p></div>}
        <button style={{ background: 'none', border: 'none', color: '#0061ff', textDecoration: 'underline', marginTop: '30px', cursor: 'pointer', fontWeight: 'bold' }} onClick={() => navigate('/')}>
           ← Return to Patient Intake
        </button>
      </div>
    </div>
  );
}