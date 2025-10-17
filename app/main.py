// Minimal Express + MySQL2 (hardcoded config, one endpoint)

const express = require("express");
const mysql = require("mysql2/promise");

const app = express();

// ==== HARD-CODED SETTINGS ====
const DB_HOST = "103.16.116.159";
const DB_PORT = 3306;
const DB_USER = "devops";
const DB_PASSWORD = "ubaya";
const DB_NAME = "movie";
const PORT = 8000;
// =============================

const pool = mysql.createPool({
  host: DB_HOST,
  port: DB_PORT,
  user: DB_USER,
  password: DB_PASSWORD,
  database: DB_NAME,
  waitForConnections: true,
  connectionLimit: 5,
  queueLimit: 0,
});

// === ENDPOINT 1: Tampilkan semua movie ===
app.get("/movies", async (_req, res) => {
  const sql = `SELECT * FROM movies LIMIT 50;`;
  let conn;
  try {
    conn = await pool.getConnection();
    const [rows] = await conn.query(sql);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: String(err) });
  } finally {
    if (conn) conn.release();
  }
});

// === ENDPOINT 2: Tampilkan movie beserta poster ===
app.get("/movies-with-poster", async (_req, res) => {
  const sql = `
    SELECT m.id, m.title, p.poster_url
    FROM movies m
    JOIN movie_poster p ON m.id = p.movie_id
    LIMIT 50;
  `;
  let conn;
  try {
    conn = await pool.getConnection();
    const [rows] = await conn.query(sql);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: String(err) });
  } finally {
    if (conn) conn.release();
  }
});

app.get("/movies/filter", async (req, res) => {
  const title = req.query.title; // ambil parameter dari URL, misal ?title=Avatar

  if (!title) {
    return res.status(400).json({ error: "Parameter 'title' wajib diisi." });
  }

  const sql = `SELECT * FROM movies WHERE title LIKE ? LIMIT 50;`;
  let conn;

  try {
    conn = await pool.getConnection();
    const [rows] = await conn.query(sql, [`%${title}%`]);
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: String(err) });
  } finally {
    if (conn) conn.release();
  }
});

app.listen(PORT, () => {
  console.log(`Movies API (Node) running on http://0.0.0.0:${PORT}`);
});
