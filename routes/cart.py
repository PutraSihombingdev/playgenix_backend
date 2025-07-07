from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required
import traceback

cart = Blueprint("cart", __name__, url_prefix="/api/v1/cart")

@cart.route("/", methods=["POST"])
@jwt_required
def add_to_cart():
    try:
        data = request.form
        user_id = g.user['user_id']
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({'error': 'product_id dan quantity wajib diisi'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (user_id, data["product_id"], data["quantity"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Produk ditambahkan ke keranjang"})
    except Exception as e:
        print("Add to cart error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Failed to add to cart'}), 500

@cart.route("/", methods=["GET"])
@jwt_required
def get_cart():
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, p.name, p.price, c.quantity, p.image_url
            FROM cart c JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(cart_items)
    except Exception as e:
        print("Get cart error:", e)
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch cart'}), 500

@cart.route("/<int:cart_id>", methods=["DELETE"])
@jwt_required
def remove_from_cart(cart_id):
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id = %s AND user_id = %s", (cart_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Item removed from cart"})
    except Exception as e:
        return jsonify({'error': 'Failed to remove from cart'}), 500