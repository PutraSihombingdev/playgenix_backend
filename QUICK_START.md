# 🚀 Quick Start Guide - PlayGenix Backend

## ⚡ Langkah Cepat untuk Testing

### 1. Setup Database
```bash
# Buat database MySQL
CREATE DATABASE playgenix;

# Import schema (jika belum)
mysql -u root -p playgenix < models/schema.sql
```

### 2. Setup Environment
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env sesuai konfigurasi database Anda
# Contoh:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=playgenix
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Backend
```bash
python run.py
```

### 5. Test Backend
```bash
# Quick test
python quick_test.py

# Atau test dengan Postman
# Import file: PlayGenix_API_Collection.json
```

## 🧪 Testing dengan Postman

### Import Collection
1. Buka Postman
2. Klik "Import"
3. Pilih file `PlayGenix_API_Collection.json`
4. Import file `PlayGenix_Environment.json`

### Test Flow
1. **Health Check** → `GET http://localhost:5000/api/health`
2. **Register** → `POST http://localhost:5000/api/auth/register`
3. **Login** → `POST http://localhost:5000/api/auth/login`
4. **Get Products** → `GET http://localhost:5000/api/products/`

## 🔧 Troubleshooting

### Error: Connection Refused
- Pastikan backend berjalan: `python run.py`
- Cek port 5000 tidak digunakan aplikasi lain

### Error: Database Connection
- Pastikan MySQL berjalan
- Cek konfigurasi di `.env`
- Pastikan database `playgenix` sudah dibuat

### Error: Module Not Found
- Install dependencies: `pip install -r requirements.txt`

### Error: JWT Token
- Cek `JWT_SECRET_KEY` di file `.env`
- Pastikan format token benar

## 📋 Expected Responses

### Health Check
```json
{
    "status": "ok",
    "message": "Backend is running",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

### Register Success
```json
{
    "message": "Register sukses"
}
```

### Login Success
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "testuser"
    }
}
```

### Get Products
```json
[
    {
        "id": 1,
        "name": "Game Test",
        "description": "Game untuk testing",
        "price": 99.99,
        "image": "https://example.com/game.jpg"
    }
]
```

## 🎯 Quick Commands

```bash
# Setup otomatis
python setup_backend.py

# Jalankan backend
python run.py

# Quick test
python quick_test.py

# Full test
python test_backend.py
```

## 📞 Support

Jika ada error, cek:
1. Log backend di terminal
2. Konfigurasi database di `.env`
3. Status MySQL server
4. Port 5000 tidak terblokir

Backend sudah siap untuk testing! 🎉 