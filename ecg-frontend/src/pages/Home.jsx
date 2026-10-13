import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="page-container">
      <div className="card" style={{ padding: '60px 40px' }}>
        <h1 style={{ fontSize: '2.5rem', color: '#0061ff', margin: '0 0 10px 0' }}>CardioAI</h1>
        <p style={{ color: '#718096', fontSize: '1.2rem', marginBottom: '40px' }}>
          Clinical-grade Deep Learning for instantaneous Myocardial Infarction detection.
        </p>
        <img 
          src="https://cdn-icons-png.flaticon.com/512/8121/8121280.png" 
          alt="Heart Icon" 
          style={{ width: '120px', marginBottom: '40px' }} 
        />
        <button className="btn-primary" onClick={() => navigate('/details')}>
          Begin Patient Diagnosis →
        </button>
      </div>
    </div>
  );
}