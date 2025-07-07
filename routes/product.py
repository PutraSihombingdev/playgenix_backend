from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required, only_admin

product = Blueprint("product", __name__, url_prefix="/api/v1/products")

@product.route("/", methods=["GET"])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch products'}), 500

@product.route("/", methods=["POST"])
@jwt_required
@only_admin
def add_product():
    try:
        data = request.form
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Name and price are required'}), 400

        # Ambil image_url dari image_url atau image
        image_url = data.get("image_url") or data.get("image") or ""

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, image_url) VALUES (%s, %s, %s, %s)",
            (data.get("name"), data.get("description", ""), data.get("price"), image_url)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Produk ditambahkan"}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add product'}), 500

@product.route("/<int:id>", methods=["PUT"])
@jwt_required
@only_admin
def update_product(id):
    try:
        data = request.form
        if not data:
            return jsonify({'error': 'Product data is required'}), 400

        # Ambil image_url dari image_url atau image
        image_url = data.get("image_url") or data.get("image") or ""

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s, image_url=%s WHERE id=%s",
            (data.get("name"), data.get("description", ""), data.get("price"), image_url, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Produk diupdate"})
    except Exception as e:
        return jsonify({'error': 'Failed to update product'}), 500

@product.route("/<int:id>", methods=["DELETE"])
@jwt_required
@only_admin
def delete_product(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Cek apakah produk ada
        cursor.execute("SELECT id FROM products WHERE id=%s", (id,))
        product = cursor.fetchone()
        if not product:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Produk tidak ditemukan'}), 404
        
        # Cek apakah produk ada di cart
        cursor.execute("SELECT id FROM cart WHERE product_id=%s", (id,))
        cart_items = cursor.fetchall()
        if cart_items:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Tidak dapat menghapus produk yang ada di keranjang'}), 400
        
        # Cek apakah produk ada di transaction_items
        cursor.execute("SELECT id FROM transaction_items WHERE product_id=%s", (id,))
        transaction_items = cursor.fetchall()
        if transaction_items:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Tidak dapat menghapus produk yang sudah ada transaksi'}), 400
        
        # Hapus produk
        cursor.execute("DELETE FROM products WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Produk dihapus"})
    except Exception as e:
        print(f"Error deleting product: {str(e)}")
        return jsonify({'error': 'Failed to delete product'}), 500