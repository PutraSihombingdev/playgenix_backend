import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { productAPI, cartAPI } from '../services/api';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Load products
      const productsResponse = await productAPI.getAllProducts();
      if (productsResponse.success) {
        setProducts(productsResponse.data);
      }

      // Load cart
      const cartResponse = await cartAPI.getCart();
      if (cartResponse.success) {
        setCart(cartResponse.data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (productId) => {
    try {
      const response = await cartAPI.addToCart(productId, 1);
      if (response.success) {
        // Reload cart data
        const cartResponse = await cartAPI.getCart();
        if (cartResponse.success) {
          setCart(cartResponse.data);
        }
        alert('Produk berhasil ditambahkan ke keranjang!');
      } else {
        alert(response.error || 'Gagal menambahkan ke keranjang');
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
      alert('Terjadi kesalahan saat menambahkan ke keranjang');
    }
  };

  const handleLogout = () => {
    logout();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">PlayGenix Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Selamat datang, {user?.username}!</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Cart Summary */}
        <div className="bg-white overflow-hidden shadow rounded-lg mb-6">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Keranjang Belanja ({cart.length} item)
            </h3>
            {cart.length > 0 ? (
              <div className="space-y-3">
                {cart.map((item) => (
                  <div key={item.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                    <div>
                      <p className="font-medium">{item.product_name}</p>
                      <p className="text-sm text-gray-600">Qty: {item.quantity}</p>
                    </div>
                    <p className="font-medium">Rp {item.price}</p>
                  </div>
                ))}
                <div className="border-t pt-3">
                  <p className="text-lg font-semibold">
                    Total: Rp {cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-gray-500">Keranjang belanja kosong</p>
            )}
          </div>
        </div>

        {/* Products */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Produk Tersedia
            </h3>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {products.map((product) => (
                <div key={product.id} className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">{product.name}</h4>
                  <p className="text-gray-600 text-sm mb-2">{product.description}</p>
                  <p className="font-medium text-indigo-600 mb-3">Rp {product.price}</p>
                  <button
                    onClick={() => handleAddToCart(product.id)}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                  >
                    Tambah ke Keranjang
                  </button>
                </div>
              ))}
            </div>
            {products.length === 0 && (
              <p className="text-gray-500 text-center py-8">Tidak ada produk tersedia</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 