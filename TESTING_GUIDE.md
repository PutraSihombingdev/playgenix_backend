# 🧪 Testing Guide - PlayGenix Backend

## 🚀 Quick Start Testing

### Option 1: Simple Test (Recommended)
```bash
# Jalankan backend
python run.py

# Di terminal lain, jalankan simple test
python simple_test.py
```

### Option 2: Quick Test
```bash
# Jalankan backend
python run.py

# Di terminal lain, jalankan quick test
python quick_test.py
```

### Option 3: Postman Test
1. Import `PlayGenix_API_Collection.json` ke Postman
2. Import `PlayGenix_Environment.json` ke Postman
3. Jalankan backend: `python run.py`
4. Test endpoint satu per satu

## 📋 Setup Sebelum Testing

### 1. Database Setup
```sql
-- Buat database
CREATE DATABASE playgenix;

-- Import schema
mysql -u root -p playgenix < models/schema.sql
```

### 2. Environment Setup
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env sesuai konfigurasi database
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=playgenix
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🧪 Test Results Expected

### Health Check
- **URL**: `GET http://localhost:5000/api/health`
- **Expected**: Status 200
- **Response**: `{"status": "ok", "message": "Backend is running"}`

### Register
- **URL**: `POST http://localhost:5000/api/auth/register`
- **Body**: `{"username": "testuser", "password": "testpass"}`
- **Expected**: Status 201 (created) atau 409 (already exists)
- **Response**: `{"message": "Register sukses"}`

### Login
- **URL**: `POST http://localhost:5000/api/auth/login`
- **Body**: `{"username": "testuser", "password": "testpass"}`
- **Expected**: Status 200
- **Response**: `{"token": "jwt_token", "user": {"id": 1, "username": "testuser"}}`

### Get Products
- **URL**: `GET http://localhost:5000/api/products/`
- **Expected**: Status 200
- **Response**: `[]` (empty array) atau array of products

## 🔧 Troubleshooting

### Error: Connection Refused
```bash
# Pastikan backend berjalan
python run.py

# Cek port 5000 tidak digunakan
netstat -an | grep 5000
```

### Error: Database Connection
```bash
# Cek MySQL berjalan
sudo service mysql status

# Cek konfigurasi database
cat .env

# Test koneksi database
python -c "from db import get_connection; conn = get_connection(); print('Database OK')"
```

### Error: Module Not Found
```bash
# Install dependencies
pip install -r requirements.txt

# Cek virtual environment
which python
pip list
```

### Error: JWT Token
```bash
# Cek JWT secret key
grep JWT_SECRET_KEY .env

# Test JWT helper
python -c "from utils.jwt_helper import generate_token; print(generate_token({'test': 'data'}))"
```

## 📊 Test Commands

```bash
# Setup otomatis
python setup_backend.py

# Jalankan backend
python run.py

# Simple test
python simple_test.py

# Quick test
python quick_test.py

# Full test
python test_backend.py
```

## 🎯 Manual Testing dengan curl

```bash
# Health check
curl -X GET http://localhost:5000/api/health

# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Get products
curl -X GET http://localhost:5000/api/products/
```

## 📝 Notes

- **Linter Errors**: Type annotation errors tidak mempengaruhi fungsionalitas runtime
- **Database**: Pastikan MySQL berjalan dan database `playgenix` sudah dibuat
- **Port**: Backend berjalan di port 5000
- **CORS**: Sudah dikonfigurasi untuk frontend
- **JWT**: Token berlaku 2 jam

## 🎉 Success Criteria

Backend dianggap berhasil jika:
1. ✅ Health check return status 200
2. ✅ Register user berhasil (201) atau user sudah ada (409)
3. ✅ Login berhasil dan return JWT token
4. ✅ Get products return array (kosong atau berisi data)

Jika semua test passed, backend siap untuk terhubung dengan frontend! 🚀 