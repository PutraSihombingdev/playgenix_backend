const API_BASE_URL = 'http://localhost:5000/api/v1';

// Helper untuk mendapatkan token dari localStorage
const getToken = () => {
  return localStorage.getItem('token');
};

// Helper untuk membuat headers dengan token
const getAuthHeaders = () => {
  const token = getToken();
  return {
    'Authorization': `Bearer ${token}`,
  };
};

// API service untuk autentikasi
export const authAPI = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    return response.json();
  },

  register: async (username, email, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      body: formData,
    });

    return response.json();
  },
};

// API service untuk produk
export const productAPI = {
  getAllProducts: async () => {
    const response = await fetch(`${API_BASE_URL}/products`);
    return response.json();
  },

  getProductById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`);
    return response.json();
  },

  createProduct: async (productData) => {
    const formData = new FormData();
    Object.keys(productData).forEach(key => {
      formData.append(key, productData[key]);
    });

    const response = await fetch(`${API_BASE_URL}/products`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });

    return response.json();
  },

  updateProduct: async (id, productData) => {
    const formData = new FormData();
    Object.keys(productData).forEach(key => {
      formData.append(key, productData[key]);
    });

    const response = await fetch(`${API_BASE_URL}/products/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: formData,
    });

    return response.json();
  },

  deleteProduct: async (id) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });

    return response.json();
  },
};

// API service untuk cart
export const cartAPI = {
  getCart: async () => {
    const response = await fetch(`${API_BASE_URL}/cart`, {
      headers: getAuthHeaders(),
    });
    return response.json();
  },

  addToCart: async (productId, quantity = 1) => {
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);

    const response = await fetch(`${API_BASE_URL}/cart/add`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });

    return response.json();
  },

  updateCartItem: async (cartId, quantity) => {
    const formData = new FormData();
    formData.append('quantity', quantity);

    const response = await fetch(`${API_BASE_URL}/cart/${cartId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: formData,
    });

    return response.json();
  },

  removeFromCart: async (cartId) => {
    const response = await fetch(`${API_BASE_URL}/cart/${cartId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });

    return response.json();
  },

  clearCart: async () => {
    const response = await fetch(`${API_BASE_URL}/cart/clear`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });

    return response.json();
  },
};

// API service untuk transaksi
export const transactionAPI = {
  createTransaction: async (paymentMethod) => {
    const formData = new FormData();
    formData.append('payment_method', paymentMethod);

    const response = await fetch(`${API_BASE_URL}/transactions`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData,
    });

    return response.json();
  },

  getTransactions: async () => {
    const response = await fetch(`${API_BASE_URL}/transactions`, {
      headers: getAuthHeaders(),
    });
    return response.json();
  },

  getTransactionById: async (id) => {
    const response = await fetch(`${API_BASE_URL}/transactions/${id}`, {
      headers: getAuthHeaders(),
    });
    return response.json();
  },
}; 