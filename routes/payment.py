from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required, only_admin

payment = Blueprint('payment', __name__, url_prefix="/api/v1/payment")

@payment.route('/', methods=['POST'])
@jwt_required
def create_payment():
    try:
        data = request.form
        user_id = g.user['user_id']
        if not data or 'amount' not in data or 'method' not in data:
            return jsonify({'error': 'amount dan method wajib diisi'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO payments (user_id, amount, method, status, created_at) VALUES (%s, %s, %s, %s, NOW())",
                       (user_id, data['amount'], data['method'], 'pending'))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Payment created'}), 201
    except Exception as e:
        print("Create payment error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to create payment'}), 500

@payment.route('/', methods=['GET'])
@jwt_required
def get_user_payments():
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, amount, method, created_at FROM payments WHERE user_id = %s", (user_id,))
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(payments)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch payments'}), 500

@payment.route('/all', methods=['GET'])
@jwt_required
@only_admin
def get_all_payments():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM payments")
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(payments)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch all payments'}), 500

@payment.route('/<int:transaction_id>', methods=['GET'])
@jwt_required
def get_payment_by_transaction(transaction_id):
    try:
        user_id = g.user['user_id']
        user_role = g.user.get('role')
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if user_role == 'admin':
            cursor.execute("SELECT * FROM payments WHERE transaction_id = %s", (transaction_id,))
        else:
            # Cek apakah transaksi milik user
            cursor.execute("SELECT t.id FROM transactions t WHERE t.id = %s AND t.user_id = %s", (transaction_id, user_id))
            trx = cursor.fetchone()
            if not trx:
                cursor.close()
                conn.close()
                return jsonify({'error': 'Tidak boleh akses pembayaran transaksi orang lain'}), 403
            cursor.execute("SELECT * FROM payments WHERE transaction_id = %s", (transaction_id,))
        payment = cursor.fetchone()
        cursor.close()
        conn.close()
        if not payment:
            return jsonify({'error': 'Pembayaran tidak ditemukan'}), 404
        return jsonify(payment)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch payment detail'}), 500

@payment.route('/<int:transaction_id>', methods=['PATCH'])
@jwt_required
def update_payment_status(transaction_id):
    try:
        user_role = g.user.get('role')
        data = request.form
        if 'status' not in data:
            return jsonify({'error': 'Status wajib diisi'}), 400
        # Hanya admin yang boleh update status ke paid/failed, user hanya boleh update ke pending
        if user_role != 'admin' and data['status'] != 'pending':
            return jsonify({'error': 'User hanya boleh update ke status pending'}), 403
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE payments SET status = %s WHERE transaction_id = %s", (data['status'], transaction_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Status pembayaran diupdate'})
    except Exception as e:
        return jsonify({'error': 'Failed to update payment status'}), 500