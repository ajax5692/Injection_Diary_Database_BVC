const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const app = express();
const port = 3000;

// Middleware to handle JSON data from the browser
app.use(express.json());

// Serve your HTML files from the current folder
app.use(express.static(__dirname));

// The path to your shared database file
// Docker maps this to /app/data/injection_diary.db
const dbPath = process.env.DB_PATH || path.join(__dirname, '..', 'data', 'injection_diary.db');

// --- 1. LOGIN ROUTE ---
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    // Hardcoded credentials for your private tool
    if (username === "abc.xyz" && password === "admin") {
        res.json({ success: true, redirect: '/dashboard.html' });
    } else {
        res.status(401).json({ success: false, message: "Invalid credentials" });
    }
});

// --- 2. QUERY ROUTE (The "DBeaver" Logic) ---
app.post('/execute-sql', (req, res) => {
    const { query } = req.body;
    
    const db = new sqlite3.Database(dbPath, (err) => {
        if (err) return res.status(500).json({ error: err.message });
    });

    // We use .all() to get all rows back for SELECT queries
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(400).json({ error: err.message });
        } else {
            res.json(rows);
        }
    });

    db.close();
});

app.listen(port, () => {
    console.log(`Web Server running at http://localhost:${port}`);
    console.log(`Connecting to database at: ${dbPath}`);
});