from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required

review = Blueprint('review', __name__, url_prefix='/api/v1/review')

@review.route('/', methods=['POST'])
@jwt_required
def add_review():
    data = request.get_json()
    user_id = g.user['user_id']
    rating = data.get('rating')
    comment = data.get('comment')
    if not comment:
        return jsonify({'error': 'Komentar wajib diisi'}), 400
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO review (user_id, rating, comment) VALUES (%s, %s, %s)",
            (user_id, rating, comment)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Review berhasil ditambahkan'})
    except Exception as e:
        print(f"Add review error: {e}")
        return jsonify({'error': 'Gagal menambahkan review'}), 500

@review.route('/', methods=['GET'])
def get_reviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id, r.user_id, u.username, u.email, r.rating, r.comment, r.created_at
            FROM review r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.created_at DESC
        """)
        reviews = cursor.fetchall()
        result = []
        for rv in reviews:
            if not isinstance(rv, dict):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rv = dict(zip(columns, rv))
            result.append({
                "id": rv["id"],
                "user_id": rv["user_id"],
                "username": rv["username"],
                "email": rv["email"],
                "rating": rv["rating"],
                "comment": rv["comment"],
                "created_at": rv["created_at"],
            })
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print(f"Get reviews error: {e}")
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