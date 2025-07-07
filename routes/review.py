from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required, only_user

review = Blueprint('review', __name__, url_prefix="/api/v1/review")

@review.route('/', methods=['POST'])
@jwt_required
@only_user
def add_review():
    try:
        user_id = g.user['user_id']
        data = request.form
        product_id = data.get('product_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        if not product_id or not rating:
            return jsonify({'error': 'product_id dan rating wajib diisi'}), 400
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating harus 1-5'}), 400
        except Exception:
            return jsonify({'error': 'Rating harus angka 1-5'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO review (user_id, product_id, rating, comment) VALUES (%s, %s, %s, %s)",
                       (user_id, product_id, rating, comment))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Review berhasil ditambahkan'}), 201
    except Exception as e:
        return jsonify({'error': 'Gagal menambah review'}), 500

@review.route('/', methods=['GET'])
def get_all_reviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM review")
        reviews = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': 'Gagal mengambil review'}), 500

@review.route('/<int:product_id>', methods=['GET'])
def get_reviews_by_product(product_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM review WHERE product_id = %s", (product_id,))
        reviews = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': 'Gagal mengambil review produk'}), 500 