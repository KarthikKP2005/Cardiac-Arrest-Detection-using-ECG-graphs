const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/predict', (req, res) => {
    const patientData = req.body;
    const pythonProcess = spawn('python', ['predict_logic.py', JSON.stringify(patientData)]);

    let dataToSend = ''; // A bucket to collect all Python output

    // 1. Collect the data chunks as they arrive
    pythonProcess.stdout.on('data', (data) => {
        dataToSend += data.toString();
    });

    // 2. Wait until Python completely finishes closing
    pythonProcess.on('close', (code) => {
        try {
            // Find where the actual JSON dictionary starts, ignoring the loading bar
            const jsonStartIndex = dataToSend.indexOf('{');
            if (jsonStartIndex === -1) throw new Error("No JSON found");
            
            const cleanJson = dataToSend.substring(jsonStartIndex);
            
            // Send the clean JSON back to React ONCE
            res.send(cleanJson);
        } catch (error) {
            console.error("Failed to parse Python output:", dataToSend);
            res.status(500).send({ error: "Failed to read AI data" });
        }
    });

    // 3. Log any red warnings in the terminal, but don't crash the server
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Warning: ${data}`);
    });
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));