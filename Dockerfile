# Lokasi: movies-api-python/Dockerfile

# 1. Gunakan base image Python
FROM python:3.9-slim

# 2. Atur direktori kerja di dalam container
WORKDIR /app

# 3. Salin file requirements dari subfolder 'app'
COPY ./app/requirements.txt .

# 4. Install semua library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# 5. Salin semua kode dari subfolder 'app'
COPY ./app .

# 6. Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]