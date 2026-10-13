import { useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    age: 60, anaemia: 0, creatinine_phosphokinase: 250, diabetes: 0,
    ejection_fraction: 38, high_blood_pressure: 0, platelets: 263358,
    serum_creatinine: 1.1, serum_sodium: 137, sex: 1, smoking: 0, time: 130
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) });
  };

 const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData);
      console.log("BACKEND RESPONSE:", response.data); // 👈 ADD THIS LINE
      setResult(response.data);
    } catch (error) {
      console.error("AXIOS ERROR:", error); // 👈 ADD THIS LINE
      setResult({ error: "Failed to connect to the AI model." });
    }
    setLoading(false);
  };

  return (
    <div className="container" style={{ padding: '20px', fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#2c3e50' }}>🫀 Explainable AI: Cardiac Arrest Predictor</h1>
      <p style={{ textAlign: 'center' }}>Enter patient vitals to generate a real-time AI risk assessment.</p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', background: '#f8f9fa', padding: '20px', borderRadius: '10px' }}>
          {Object.keys(formData).map((key) => (
            <label key={key} style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 'bold' }}>
              {key.replace(/_/g, ' ').toUpperCase()}:
              <input type="number" step="any" name={key} value={formData[key]} onChange={handleChange} style={{ width: '80px', padding: '5px' }} />
            </label>
          ))}
          <button type="submit" disabled={loading} style={{ gridColumn: 'span 2', padding: '15px', background: '#007bff', color: 'white', border: 'none', borderRadius: '5px', fontSize: '18px', cursor: 'pointer' }}>
            {loading ? 'Analyzing...' : 'Run AI Prediction'}
          </button>
        </form>

        {result && !result.error && (
          <div style={{ background: '#fff', border: '2px solid #eee', padding: '20px', borderRadius: '10px', textAlign: 'center' }}>
            <h2>AI Analysis Complete</h2>
            <h1 style={{ color: result.prediction === 'High Risk' ? '#dc3545' : '#28a745', margin: '10px 0' }}>
              {result.prediction} ({result.risk_score}%)
            </h1>
            
            <hr style={{ margin: '20px 0' }} />
            
            <h3>🧠 Why did the AI make this decision?</h3>
            <p style={{ color: '#666', fontSize: '14px' }}>Positive impact increases risk (Red). Negative impact decreases risk (Blue).</p>
            
            <div style={{ height: '300px', width: '100%', marginTop: '20px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart layout="vertical" data={result.explanations} margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="Impact" radius={[0, 4, 4, 0]}>
                    {result.explanations.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.Impact > 0 ? '#ff4d4f' : '#40a9ff'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App