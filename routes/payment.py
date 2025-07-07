from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required

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