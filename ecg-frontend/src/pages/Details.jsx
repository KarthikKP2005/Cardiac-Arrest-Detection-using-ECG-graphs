import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Details() {
  const navigate = useNavigate();
  
  // 1. State is defined up here, outside the return block!
  const [patient, setPatient] = useState({ name: '', age: '', gender: 'Male', id: '', complaint: '' });

  const handleNext = (e) => {
    e.preventDefault();
    navigate('/analyze', { state: { patient } });
  };

  return (
    <div className="page-container">
      <div className="card">
        <h2 style={{ color: '#2d3748', marginBottom: '30px' }}>Patient Intake Form</h2>
        <form onSubmit={handleNext}>
          
          <div className="input-group">
            <label>Patient ID</label>
            <input required type="text" placeholder="e.g. PTB-8472" 
                   onChange={e => setPatient({...patient, id: e.target.value})} />
          </div>

          <div className="input-group">
            <label>Full Name</label>
            <input required type="text" placeholder="John Doe" 
                   onChange={e => setPatient({...patient, name: e.target.value})} />
          </div>

          <div style={{ display: 'flex', gap: '20px' }}>
            <div className="input-group" style={{ flex: 1 }}>
              <label>Age</label>
              <input required type="number" placeholder="45" 
                     onChange={e => setPatient({...patient, age: e.target.value})} />
            </div>
            <div className="input-group" style={{ flex: 1 }}>
              <label>Gender</label>
              <select onChange={e => setPatient({...patient, gender: e.target.value})}>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          {/* 2. Chief Complaint field added cleanly inside the form */}
          <div className="input-group">
            <label>Chief Complaint (Symptoms)</label>
            <input required type="text" placeholder="e.g., Severe chest pain, shortness of breath..." 
                   onChange={e => setPatient({...patient, complaint: e.target.value})} />
          </div>

          <button type="submit" className="btn-primary">Proceed to ECG Upload</button>
        </form>
      </div>
    </div>
  );
}