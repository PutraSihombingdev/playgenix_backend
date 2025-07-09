import os
import time
from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required
from config import Config

transaction = Blueprint("transaction", __name__, url_prefix="/api/v1/transaction")

@transaction.route("/", methods=["POST"])
@jwt_required
def create_transaction():
    conn = None
    cursor = None
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT SUM(p.price * c.quantity) as total
            FROM cart c JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        row = cursor.fetchone()
        import decimal
        if row is None:
            total = 0.0
        elif isinstance(row, dict):
            val = row.get('total')
            if val is None:
                total = 0.0
            elif isinstance(val, (int, float)):
                total = float(val)
            elif isinstance(val, decimal.Decimal):
                total = float(val)
            else:
                total = 0.0
        elif isinstance(row, (list, tuple)):
            val = row[0]
            if val is None:
                total = 0.0
            elif isinstance(val, (int, float)):
                total = float(val)
            elif isinstance(val, decimal.Decimal):
                total = float(val)
            else:
                total = 0.0
        else:
            total = 0.0

        if total == 0.0:
            return jsonify({'error': 'Keranjang kosong!'}), 400

        # Buat transaksi
        cursor.execute(
            "INSERT INTO transactions (user_id, total, status) VALUES (%s, %s, %s)",
            (user_id, total, 'pending')
        )
        transaction_id = cursor.lastrowid

        # Buat payment (WAJIB isi payment_method)
        cursor.execute(
            "INSERT INTO payments (transaction_id, user_id, payment_method, amount, status) VALUES (%s, %s, %s, %s, %s)",
            (transaction_id, user_id, 'manual', total, 'pending')
        )

        # Ambil semua item di keranjang user beserta harga produk
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        print("cart_items:", cart_items)

        # (Opsional) Kosongkan keranjang user
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

        # Masukkan setiap item ke tabel transaction_items (dengan harga saat transaksi)
        for item in cart_items:
            print("item:", item)
            # Pastikan item adalah dict
            if not isinstance(item, dict):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                item = dict(zip(columns, item))
            # Pastikan semua field bertipe dasar numerik
            try:
                if not isinstance(item['product_id'], (int, float, str, decimal.Decimal)):
                    continue
                if not isinstance(item['quantity'], (int, float, str, decimal.Decimal)):
                    continue
                if not isinstance(item['price'], (int, float, str, decimal.Decimal)):
                    continue
                product_id = int(item['product_id'])
                quantity = int(item['quantity'])
                price = float(item['price'])
            except (ValueError, TypeError, KeyError):
                continue  # skip jika gagal konversi
            cursor.execute(
                "INSERT INTO transaction_items (transaction_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (transaction_id, product_id, quantity, price)
            )

        conn.commit()
        return jsonify({"transaction_id": transaction_id, "amount": total}), 201
    except Exception as e:
        print("Create transaction error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to create transaction'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@transaction.route('/upload-bukti', methods=['POST'])
@jwt_required
def upload_bukti():
    user_id = g.user['user_id']
    transaction_id = request.form.get('transaction_id')
    amount = request.form.get('amount')
    file = request.files.get('bukti')

    # Validasi
    if not transaction_id or not amount:
        return jsonify({'error': 'transaction_id dan amount wajib diisi'}), 400
    if not file or not hasattr(file, 'filename') or not file.filename:
        return jsonify({'error': 'Bukti transfer wajib diupload'}), 400
    if '.' not in file.filename:
        return jsonify({'error': 'Nama file tidak valid'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File harus berupa gambar (jpg, jpeg, png)'}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{user_id}_{transaction_id}_{int(time.time())}.{ext}"
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    # Simpan file
    try:
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(file_path)
        print(f"File saved to: {file_path}")
    except Exception as e:
        print("File save error:", e)
        return jsonify({'error': 'Gagal menyimpan file bukti transfer'}), 500

    # Update payment di database
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE payments SET bukti_transfer=%s, amount=%s WHERE transaction_id=%s AND user_id=%s",
            (file_path, float(amount), transaction_id, user_id)
        )
        conn.commit()
        print(f"Payment updated for transaction_id={transaction_id}, user_id={user_id}")
    except Exception as e:
        print("DB update error:", e)
        return jsonify({'error': 'Gagal update data pembayaran di database'}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return jsonify({'message': 'Bukti transfer berhasil diupload', 'file_path': file_path}), 201

# Contoh di Flask (gunakan cursor dictionary=True)
@transaction.route('/<int:transaction_id>', methods=['GET'])
@jwt_required
def get_transaction_detail(transaction_id):
    try:
        role = g.user.get('role')
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Admin bisa akses semua transaksi, user hanya miliknya sendiri
        if role == 'admin':
            cursor.execute("""
                SELECT t.*, u.email, p.bukti_transfer, p.status as payment_status
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                LEFT JOIN payments p ON p.transaction_id = t.id
                LEFT JOIN transaction_items ti ON ti.transaction_id = t.id
                WHERE t.id = %s
                LIMIT 1
            """, (transaction_id,))
        else:
            user_id = g.user['user_id']
            cursor.execute("""
                SELECT t.*, u.email, p.bukti_transfer, p.status as payment_status
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                LEFT JOIN payments p ON p.transaction_id = t.id
                LEFT JOIN transaction_items ti ON ti.transaction_id = t.id
                WHERE t.id = %s AND t.user_id = %s
                LIMIT 1
            """, (transaction_id, user_id))
        trx = cursor.fetchone()
        cursor.close()
        conn.close()
        if not trx:
            return jsonify({'error': 'Transaksi tidak ditemukan'}), 404

        # Pastikan hasilnya dict agar bisa pakai .get()
        if not isinstance(trx, dict):
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            trx = dict(zip(columns, trx))

        response = {
            "id": trx.get("id"),
            "email": trx.get("email"),
            "total": trx.get("total"),
            # Ambil description produk dari item pertama
            "description": "-",
            "bukti_pembayaran": trx.get("bukti_transfer"),
            "status": trx.get("payment_status"),
            "created_at": trx.get("created_at"),
        }
        # Query description produk untuk detail transaksi
        trx_id = trx.get("id")
        description = "-"
        if isinstance(trx_id, int):
            cursor2 = get_connection().cursor(dictionary=True)
            cursor2.execute("""
                SELECT p.description
                FROM transaction_items ti
                JOIN products p ON ti.product_id = p.id
                WHERE ti.transaction_id = %s
                LIMIT 1
            """, (trx_id,))
            item = cursor2.fetchone()
            if isinstance(item, dict) and "description" in item:
                description = item["description"]
            cursor2.close()
        response["description"] = description
        return jsonify(response)
    except Exception as e:
        print("Get transaction detail error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to fetch transaction detail'}), 500


        # Pastikan hasilnya dict Python biasa
        if isinstance(trx, dict):
            response = {k: v for k, v in trx.items()}
        else:
            # fallback: ambil nama kolom dari cursor.description
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            response = {col: val for col, val in zip(columns, trx)}

        # Ambil payment terkait transaksi ini
        cursor.execute("SELECT * FROM payments WHERE transaction_id=%s", (transaction_id,))
        payment = cursor.fetchone()
        if payment is not None and not isinstance(payment, dict):
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            payment = {col: val for col, val in zip(columns, payment)}
        response['payment'] = to_json_safe(payment) if payment is not None else None  # type: ignore
        cursor.close()
        conn.close()
        return jsonify(response)

@transaction.route('/<int:transaction_id>/status', methods=['PATCH'])
@jwt_required
def update_transaction_status(transaction_id):
    if g.user.get('role') != 'admin':
        return jsonify({'error': 'Akses hanya untuk admin'}), 403
    if not request.is_json or not request.json or 'status' not in request.json:
        return jsonify({'error': 'Status wajib diisi'}), 400
    status = request.json.get('status')
    print(f"Received status: {status}")  # Debug print
    if status not in ['pending', 'paid', 'failed']:
        print(f"Invalid status: {status}. Allowed: ['pending', 'paid', 'failed']")  # Debug print
        return jsonify({'error': 'Status tidak valid'}), 400
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE payments SET status=%s WHERE transaction_id=%s", (status, transaction_id))
        conn.commit()
        print(f"Status updated successfully: transaction_id={transaction_id}, status={status}")
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return jsonify({'error': 'Gagal update status'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return jsonify({'message': 'Status updated'})

@transaction.route('/list', methods=['GET'])
@jwt_required
def list_transactions():
    try:
        # Cek role user
        if g.user.get('role') != 'admin':
            return jsonify({'error': 'Akses hanya untuk admin'}), 403

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Ambil semua transaksi beserta email user, deskripsi akun, dan bukti pembayaran
        cursor.execute("""
            SELECT t.id, t.total, t.status, t.created_at,
                   u.email,
                   p.bukti_transfer, p.status as payment_status
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            LEFT JOIN payments p ON p.transaction_id = t.id
            LEFT JOIN transaction_items ti ON ti.transaction_id = t.id
            ORDER BY t.created_at DESC
        """)
        transactions = cursor.fetchall()
        result = []
        for trx in transactions:
            if not isinstance(trx, dict):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                trx = dict(zip(columns, trx))
            # Ambil description produk dari item pertama
            trx_id = trx.get("id")
            description = "-"
            if isinstance(trx_id, int):
                cursor2 = conn.cursor(dictionary=True)
                cursor2.execute("""
                    SELECT p.description
                    FROM transaction_items ti
                    JOIN products p ON ti.product_id = p.id
                    WHERE ti.transaction_id = %s
                    LIMIT 1
                """, (trx_id,))
                item = cursor2.fetchone()
                if isinstance(item, dict) and "description" in item:
                    description = item["description"]
                cursor2.close()
            result.append({
                "id": trx.get("id"),
                "email": trx.get("email"),
                "total": trx.get("total"),
                "description": description,
                "bukti_pembayaran": trx.get("bukti_transfer"),
                "status": trx.get("payment_status") or trx.get("status"),
                "created_at": trx.get("created_at"),
            })
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print("List transactions error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to fetch transaction list'}), 500



@transaction.route('/my', methods=['GET'])
@jwt_required
def my_transactions():
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
        transactions = cursor.fetchall()
        result = []
        for trx in transactions:
            # Pastikan trx adalah dict
            if not isinstance(trx, dict):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                trx = dict(zip(columns, trx))
            # Ambil payment
            payment = None
            trx_id = trx.get('id') if isinstance(trx, dict) else None
            if trx_id is not None and (isinstance(trx_id, int) or (isinstance(trx_id, str) and str(trx_id).isdigit())):
                cursor.execute("SELECT * FROM payments WHERE transaction_id=%s", (trx_id,))
                payment_row = cursor.fetchone()
                if payment_row is not None and not isinstance(payment_row, dict):
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    payment = {col: val for col, val in zip(columns, payment_row)}
                else:
                    payment = payment_row
            # Ambil deskripsi produk dari item pertama
            description = "-"
            if trx_id is not None and (isinstance(trx_id, int) or (isinstance(trx_id, str) and str(trx_id).isdigit())):
                cursor2 = conn.cursor(dictionary=True)
                cursor2.execute("""
                    SELECT p.description
                    FROM transaction_items ti
                    JOIN products p ON ti.product_id = p.id
                    WHERE ti.transaction_id = %s
                    LIMIT 1
                """, (trx_id,))
                item = cursor2.fetchone()
                if isinstance(item, dict) and "description" in item:
                    description = item["description"]
                cursor2.close()
            # Gabungkan hasil
            result.append({
                "id": trx.get("id"),
                "total": trx.get("total"),
                "status": payment.get("status") if payment else trx.get("status"),
                "created_at": trx.get("created_at"),
                "description": description,
                "bukti_pembayaran": payment.get("bukti_transfer") if payment else None,
                "payment": to_json_safe(payment) if payment is not None else None,
            })
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print("My transactions error:", e)
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Failed to fetch my transactions'}), 500

@transaction.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required
def delete_transaction(transaction_id):
    if g.user.get('role') != 'admin':
        return jsonify({'error': 'Akses hanya untuk admin'}), 403
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Hapus payment terkait
        cursor.execute("DELETE FROM payments WHERE transaction_id=%s", (transaction_id,))
        # Hapus item transaksi terkait
        cursor.execute("DELETE FROM transaction_items WHERE transaction_id=%s", (transaction_id,))
        # Hapus transaksi
        cursor.execute("DELETE FROM transactions WHERE id=%s", (transaction_id,))
        conn.commit()
        return jsonify({'message': 'Transaksi berhasil dihapus'})
    except Exception as e:
        print(f"Delete transaction error: {e}")
        if conn:
            conn.rollback()
        return jsonify({'error': 'Gagal menghapus transaksi'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def to_json_safe(d):
    if not isinstance(d, dict):
        return None
    result = {}
    for k, v in d.items():
        if isinstance(v, (str, int, float, bool, type(None))):
            result[k] = v
        else:
            result[k] = str(v)
    return result