# Lokasi: movies-api-python/app/app.py

from flask import Flask, jsonify, request
import mysql.connector

# ==== SETTINGS DENGAN IP BARU ANDA ====
DB_HOST = "103.16.116.159"
DB_PORT = 3306
DB_USER = "devops"
DB_PASSWORD = "ubaya"
DB_NAME = "movie"
# ======================================

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

@app.get("/movies")
def get_movies():
    title_query = request.args.get('title')
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        if title_query:
            sql = "SELECT * FROM movies WHERE title LIKE %s LIMIT 50;"
            params = (f"%{title_query}%",)
            cur.execute(sql, params)
        else:
            sql = "SELECT * FROM movies LIMIT 50;"
            cur.execute(sql)

        cols = [d[0] for d in cur.description]
        data = [dict(zip(cols, row)) for row in cur.fetchall()]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cur.close(); conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)