from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required

transaction = Blueprint('transaction', __name__, url_prefix="/api/v1/transaction")

@transaction.route('/', methods=['POST'])
@jwt_required
def create_transaction():
    try:
        data = request.form
        user_id = g.user['user_id']
        if not data or 'payment_id' not in data or 'total' not in data:
            return jsonify({'error': 'payment_id dan total wajib diisi'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id, payment_id, total, created_at) VALUES (%s, %s, %s, NOW())",
            (user_id, data['payment_id'], data['total'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Transaction created'}), 201
    except Exception as e:
        print("Create transaction error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to create transaction'}), 500

@transaction.route('/', methods=['GET'])
@jwt_required
def get_transactions():
    # Mengambil semua transaksi milik user
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, total, payment_id, created_at FROM transactions WHERE user_id = %s", (user_id,))
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(transactions)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch transactions'}), 500

@transaction.route('/<int:id>', methods=['GET'])
@jwt_required
def get_transaction_by_id(id):
    # Mengambil transaksi tertentu
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE id = %s AND user_id = %s", (id, user_id))
        transaction = cursor.fetchone()
        cursor.close()
        conn.close()
        if transaction:
            return jsonify(transaction)
        else:
            return jsonify({'error': 'Transaction not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to fetch transaction by ID'}), 500
