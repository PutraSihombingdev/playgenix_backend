# PlayGenix Backend

Backend API untuk aplikasi PlayGenix yang dapat terhubung dengan frontend.

## Fitur

- ✅ Authentication (Register/Login)
- ✅ Product Management (CRUD)
- ✅ Shopping Cart
- ✅ Payment Processing
- ✅ Transaction History
- ✅ CORS Support untuk Frontend
- ✅ JWT Token Authentication
- ✅ MySQL Database Integration

## Setup dan Instalasi

### 1. Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

### 2. Clone Repository

```bash
git clone <repository-url>
cd playgenix_backend
```

### 3. Setup Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

1. Buat database MySQL:
```sql
CREATE DATABASE playgenix;
```

2. Import schema database:
```bash
mysql -u root -p playgenix < models/schema.sql
```

### 6. Environment Configuration

1. Copy file environment template:
```bash
cp env_example.txt .env
```

2. Edit file `.env` sesuai konfigurasi database Anda:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=playgenix
JWT_SECRET_KEY=your-super-secret-jwt-key
FLASK_SECRET_KEY=your-super-secret-flask-key
```

### 7. Run Application

```bash
python run.py
```

Server akan berjalan di `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user baru
- `POST /api/auth/login` - Login user

### Products
- `GET /api/products/` - Ambil semua produk
- `POST /api/products/` - Tambah produk baru
- `PUT /api/products/<id>` - Update produk
- `DELETE /api/products/<id>` - Hapus produk

### Cart
- `GET /api/cart/<user_id>` - Ambil cart user
- `POST /api/cart/` - Tambah item ke cart
- `DELETE /api/cart/<cart_id>` - Hapus item dari cart

### Payment
- `POST /api/payment/` - Buat payment baru
- `GET /api/payment/<user_id>` - Ambil payment history user

### Transaction
- `POST /api/transaction/` - Buat transaction baru
- `GET /api/transaction/<user_id>` - Ambil transaction history user

### Health Check
- `GET /api/health` - Cek status backend

## Koneksi Frontend

Backend sudah dikonfigurasi dengan CORS untuk menerima request dari frontend yang berjalan di:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

## Contoh Request

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Login User
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Get Products
```bash
curl -X GET http://localhost:5000/api/products/
```

## Troubleshooting

### Error Database Connection
- Pastikan MySQL server berjalan
- Periksa konfigurasi database di file `.env`
- Pastikan database `playgenix` sudah dibuat

### Error CORS
- Pastikan frontend berjalan di port yang diizinkan (3000 atau 5173)
- Periksa konfigurasi CORS di `config.py`

### Error JWT
- Pastikan `JWT_SECRET_KEY` sudah diset di file `.env`

## Development

Untuk development, gunakan:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python run.py
```

## Production

Untuk production, pastikan:
- Set `FLASK_ENV=production`
- Set `FLASK_DEBUG=False`
- Gunakan secret key yang kuat
- Konfigurasi database production
- Setup proper CORS origins