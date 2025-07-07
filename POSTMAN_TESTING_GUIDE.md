# 🧪 Panduan Testing PlayGenix Backend dengan Postman

## 📋 Setup Postman

### 1. Import Collection dan Environment

1. **Import Collection:**
   - Buka Postman
   - Klik "Import" 
   - Pilih file `PlayGenix_API_Collection.json`
   - Collection akan muncul di sidebar

2. **Import Environment:**
   - Klik "Import" lagi
   - Pilih file `PlayGenix_Environment.json`
   - Pilih environment "PlayGenix Environment" di dropdown

### 2. Setup Database

Sebelum testing, pastikan database sudah siap:

```sql
-- Buat database
CREATE DATABASE IF NOT EXISTS playgenix;

-- Import schema
mysql -u root -p playgenix < models/schema.sql
```

### 3. Setup Environment Variables

Di Postman Environment, pastikan:
- `base_url`: `http://localhost:5000`
- `auth_token`: (akan diisi otomatis setelah login)
- `user_id`: `1`
- `product_id`: `1`
- `payment_id`: `1`

## 🚀 Langkah Testing

### Step 1: Health Check
**Request:** `GET {{base_url}}/api/health`

**Expected Response:**
```json
{
    "status": "ok",
    "message": "Backend is running",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

### Step 2: Register User
**Request:** `POST {{base_url}}/api/auth/register`

**Body:**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Expected Response:**
```json
{
    "message": "Register sukses"
}
```

### Step 3: Login User
**Request:** `POST {{base_url}}/api/auth/login`

**Body:**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Expected Response:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "testuser"
    }
}
```

**Setelah login berhasil:**
- Copy token dari response
- Paste ke environment variable `auth_token`

### Step 4: Add Product
**Request:** `POST {{base_url}}/api/products/`

**Body:**
```json
{
    "name": "Game Test",
    "description": "Game untuk testing",
    "price": 99.99,
    "image": "https://example.com/game.jpg"
}
```

**Expected Response:**
```json
{
    "message": "Produk ditambahkan"
}
```

### Step 5: Get All Products
**Request:** `GET {{base_url}}/api/products/`

**Expected Response:**
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

### Step 6: Add to Cart
**Request:** `POST {{base_url}}/api/cart/`

**Body:**
```json
{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
}
```

**Expected Response:**
```json
{
    "message": "Produk ditambahkan ke keranjang"
}
```

### Step 7: Get User Cart
**Request:** `GET {{base_url}}/api/cart/1`

**Expected Response:**
```json
[
    {
        "id": 1,
        "name": "Game Test",
        "price": 99.99,
        "quantity": 2,
        "image": "https://example.com/game.jpg"
    }
]
```

### Step 8: Create Payment
**Request:** `POST {{base_url}}/api/payment/`

**Body:**
```json
{
    "user_id": 1,
    "amount": 199.98,
    "method": "credit_card"
}
```

**Expected Response:**
```json
{
    "message": "Payment created"
}
```

### Step 9: Create Transaction
**Request:** `POST {{base_url}}/api/transaction/`

**Body:**
```json
{
    "user_id": 1,
    "payment_id": 1,
    "total": 199.98
}
```

**Expected Response:**
```json
{
    "message": "Transaction created"
}
```

## 🔧 Troubleshooting

### Error: Connection Refused
- Pastikan backend berjalan: `python run.py`
- Cek URL di environment: `http://localhost:5000`

### Error: Database Connection
- Pastikan MySQL berjalan
- Cek konfigurasi database di `.env`
- Pastikan database `playgenix` sudah dibuat

### Error: 404 Not Found
- Cek URL endpoint
- Pastikan route sudah terdaftar di `app.py`

### Error: 500 Internal Server Error
- Cek log backend untuk detail error
- Pastikan semua dependencies terinstall

## 📊 Test Flow Lengkap

1. **Health Check** → Pastikan backend running
2. **Register** → Buat user baru
3. **Login** → Dapatkan token
4. **Add Product** → Tambah produk
5. **Get Products** → Lihat semua produk
6. **Add to Cart** → Tambah ke keranjang
7. **Get Cart** → Lihat keranjang
8. **Create Payment** → Buat pembayaran
9. **Create Transaction** → Buat transaksi
10. **Get Transactions** → Lihat history transaksi

## 🎯 Tips Testing

- **Gunakan Environment Variables** untuk data yang berubah
- **Test Error Cases** dengan data invalid
- **Check Response Headers** untuk CORS
- **Verify JSON Format** response
- **Test dengan Data Berbeda** untuk memastikan validasi

## 📝 Notes

- Backend berjalan di `http://localhost:5000`
- Database: MySQL dengan nama `playgenix`
- JWT token berlaku 2 jam
- CORS sudah dikonfigurasi untuk frontend
- Semua response dalam format JSON 