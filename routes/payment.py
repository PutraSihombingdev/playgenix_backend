import os
from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required
from werkzeug.utils import secure_filename

payment = Blueprint('payment', __name__, url_prefix="/api/v1/payment")

UPLOAD_FOLDER = 'uploads/payments'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@payment.route('/rekening', methods=['GET'])
def get_rekening():
    rekening = {
        "bank": "BCA",
        "no_rekening": "1234567890",
        "nama": "PT PlayGenix Indonesia"
    }
    return jsonify(rekening), 200

@payment.route('/upload-bukti', methods=['POST'])
@jwt_required
def upload_bukti():
    try:
        user_id = g.user['user_id']
        amount = request.form.get('amount')
        transaction_id = request.form.get('transaction_id')
        file = request.files.get('bukti')

        if not amount or not transaction_id or not file:
            return jsonify({'error': 'amount, transaction_id, dan file bukti wajib diisi'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Format file tidak didukung'}), 400

        filename = f"{transaction_id}_{user_id}_{file.filename}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Update database payments
        conn = get_connection()
        cursor = conn.cursor()
        # Pastikan payment_method diisi (misal: 'manual')
        cursor.execute(
            "UPDATE payments SET amount=%s, bukti_transfer=%s, payment_method=%s, status='pending' WHERE transaction_id=%s AND user_id=%s",
            (amount, filename, 'manual', transaction_id, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Bukti pembayaran berhasil diupload!'}), 200
    except Exception as e:
        print("Upload bukti error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Gagal upload bukti pembayaran'}), 500 

@payment.route('/', methods=['GET'])
@jwt_required
def get_payments():
    user_id = g.user['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(payments) 

@payment.route('/all', methods=['GET'])
@jwt_required
def get_all_payments():
    # Hanya admin yang boleh akses
    if g.user.get('role') != 'admin':
        return jsonify({'error': 'Akses hanya untuk admin'}), 403
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM payments ORDER BY created_at DESC")
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(payments)
        
        