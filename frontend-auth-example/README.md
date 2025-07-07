# PlayGenix Frontend - Integrasi dengan Backend Flask

Proyek ini adalah frontend React untuk aplikasi PlayGenix yang terintegrasi dengan backend Flask.

## Fitur

- ✅ Autentikasi dengan JWT Token
- ✅ Login dan Register dengan Ant Design
- ✅ Protected Routes
- ✅ Integrasi dengan API Backend Flask
- ✅ Manajemen state dengan Context API
- ✅ UI yang responsif dan modern

## Struktur File

```
src/
├── components/
│   ├── LoginPage.js          # Halaman login dengan Ant Design
│   ├── RegisterPage.js       # Halaman register dengan Ant Design
│   ├── Dashboard.js          # Halaman dashboard (contoh)
│   └── ProtectedRoute.js     # Komponen untuk melindungi route
├── contexts/
│   └── AuthContext.js        # Context untuk autentikasi
├── services/
│   └── api.js               # Service untuk API calls
└── App.js                   # Komponen utama dengan routing
```

## Setup dan Instalasi

### 1. Install Dependencies

```bash
npm install
```

### 2. Pastikan Backend Flask Berjalan

Backend Flask harus berjalan di `http://localhost:5000` dengan endpoint:
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/products`
- `GET /api/v1/cart`
- dll.

### 3. Jalankan Frontend

```bash
npm start
```

Frontend akan berjalan di `http://localhost:3000`

## Integrasi dengan Backend

### AuthContext

`AuthContext` mengelola state autentikasi dan menyediakan fungsi:
- `login(username, password)` - Login user
- `register(username, email, password)` - Register user baru
- `logout()` - Logout user
- `isAuthenticated()` - Cek status autentikasi

### API Service

`api.js` berisi fungsi-fungsi untuk komunikasi dengan backend:
- `authAPI` - Untuk autentikasi
- `productAPI` - Untuk manajemen produk
- `cartAPI` - Untuk keranjang belanja
- `transactionAPI` - Untuk transaksi

## Penggunaan

### 1. Login

```javascript
import { useAuth } from '../contexts/AuthContext';

const { login } = useAuth();

const handleLogin = async (values) => {
  const result = await login(values.username, values.password);
  if (result.success) {
    // Redirect ke dashboard
    navigate('/');
  }
};
```

### 2. Protected Route

```javascript
import ProtectedRoute from '../components/ProtectedRoute';

<Route 
  path="/dashboard" 
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  } 
/>
```

### 3. API Calls dengan Token

```javascript
import { productAPI } from '../services/api';

// Token otomatis ditambahkan ke header
const products = await productAPI.getAllProducts();
```

## Konfigurasi

### URL Backend

Ubah `API_BASE_URL` di `src/services/api.js` jika backend berjalan di port berbeda:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1';
```

### CORS

Pastikan backend Flask mengizinkan CORS dari frontend:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
```

## Troubleshooting

### 1. Error CORS
- Pastikan backend mengizinkan CORS dari `http://localhost:3000`
- Install `flask-cors` di backend

### 2. Error 404
- Pastikan backend berjalan di port 5000
- Cek endpoint URL di `api.js`

### 3. Error JWT
- Pastikan token tersimpan di localStorage
- Cek format Authorization header: `Bearer <token>`

### 4. Error Form Data
- Backend menggunakan `form-data`, bukan JSON
- Pastikan request menggunakan `FormData`

## Dependencies

- `react` - Framework React
- `react-router-dom` - Routing
- `antd` - UI Components
- `@ant-design/icons` - Icons

## Scripts

- `npm start` - Jalankan development server
- `npm build` - Build untuk production
- `npm test` - Jalankan tests 