from flask import Flask, jsonify, request # Diambil dari pekerjaan Anggota 2
import mysql.connector

# ==== SETTINGS (Tetap sama) ====
DB_HOST = "103.157.97.107"
DB_PORT = 3306
DB_USER = "devops"
DB_PASSWORD = "ubaya"
DB_NAME = "movie"
# =================================

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

@app.get("/movies")
def get_movies():
    # --- BAGIAN PEKERJAAN ANGGOTA 2 ---
    # Mengambil parameter 'title' dari URL
    title_query = request.args.get('title')
    
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        # Logika SQL digabungkan antara pekerjaan Anggota 1 dan 2
        if title_query:
            # Jika ada filter judul
            # Menggabungkan JOIN (Anggota 1) dan WHERE (Anggota 2)
            sql = """
                SELECT m.*, mp.poster_path
                FROM movies m
                LEFT JOIN movie_poster mp ON m.id = mp.movie_id
                WHERE m.title LIKE %s
                LIMIT 50;
            """
            params = (f"%{title_query}%",)
            cur.execute(sql, params)
        else:
            # Jika tidak ada filter, hanya menjalankan query dari Anggota 1
            # --- BAGIAN PEKERJAAN ANGGOTA 1 ---
            sql = """
                SELECT m.*, mp.poster_path
                FROM movies m
                LEFT JOIN movie_poster mp ON m.id = mp.movie_id
                LIMIT 50;
            """
            cur.execute(sql)

        # Kode ini secara otomatis menangani kolom tambahan 'poster_path'
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
