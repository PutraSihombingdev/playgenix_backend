from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import jwt_required, only_admin

transaction = Blueprint('transaction', __name__, url_prefix="/api/v1/transaction")

def dict_keys_to_str(d):
    return {str(k): v for k, v in d.items()}

@transaction.route('/', methods=['POST'])
@jwt_required
def create_transaction():
    try:
        user_id = g.user['user_id']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Ambil semua item cart user
        cart_cursor = conn.cursor(dictionary=True)
        cart_cursor.execute("SELECT product_id, quantity FROM cart WHERE user_id = %s", (user_id,))
        cart_items = cart_cursor.fetchall()
        cart_cursor.close()
        # Tidak perlu cek tuple, karena cursor dictionary=True
        if not cart_items:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Keranjang kosong'}), 400
        # Hitung total
        total = 0
        items_data = []
        for item in cart_items:
            if not isinstance(item, dict):
                continue
            # Pastikan value bukan None dan bisa di-cast ke int
            product_id_raw = item.get('product_id')
            quantity_raw = item.get('quantity')
            if product_id_raw is None or quantity_raw is None:
                continue
            try:
                product_id = int(str(product_id_raw))
                quantity = int(str(quantity_raw))
            except Exception as e:
                print(f"DEBUG: gagal cast product_id/quantity: {product_id_raw}, {quantity_raw}, error: {e}")
                continue
            prod_cursor = conn.cursor(dictionary=True)
            prod_cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            product = prod_cursor.fetchone()
            prod_cursor.close()
            if not isinstance(product, dict) or 'price' not in product:
                continue
            raw_price = product['price']
            if raw_price is None:
                continue
            try:
                price = float(str(raw_price))
            except Exception as e:
                print(f"DEBUG: gagal cast price: {raw_price}, error: {e}")
                continue
            subtotal = price * quantity
            total += subtotal
            items_data.append({
                'product_id': product_id,
                'quantity': quantity,
                'price': price
            })
        if not items_data:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Semua produk di keranjang tidak valid'}), 400
        # Insert ke transactions
        cursor.execute(
            "INSERT INTO transactions (user_id, total, status) VALUES (%s, %s, %s)",
            (user_id, total, 'pending')
        )
        transaction_id = cursor.lastrowid
        # Insert ke transaction_items
        for item in items_data:
            cursor.execute(
                "INSERT INTO transaction_items (transaction_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                (transaction_id, item['product_id'], item['quantity'], item['price'])
            )
        # Insert ke payments (status pending)
        cursor.execute(
            "INSERT INTO payments (transaction_id, payment_method, amount, status) VALUES (%s, %s, %s, %s)",
            (transaction_id, 'manual', total, 'pending')
        )
        # Kosongkan cart user
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Checkout berhasil', 'transaction_id': transaction_id, 'total': total}), 201
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Gagal checkout'}), 500

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

@transaction.route('/all', methods=['GET'])
@jwt_required
@only_admin
def get_all_transactions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(transactions)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch all transactions'}), 500

@transaction.route('/<int:id>', methods=['GET'])
@jwt_required
def get_transaction_by_id(id):
    # Mengambil transaksi tertentu beserta itemnya
    try:
        user_id = g.user['user_id']
        user_role = g.user.get('role')
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Admin bisa akses semua transaksi, user hanya miliknya
        if user_role == 'admin':
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
        else:
            cursor.execute("SELECT * FROM transactions WHERE id = %s AND user_id = %s", (id, user_id))
        transaction = cursor.fetchone()
        if not transaction:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Transaction not found'}), 404

        # Jika hasil fetchone sudah dict, gunakan langsung
        if isinstance(transaction, dict):
            transaction_dict = transaction
        else:
            # fallback: mapping kolom ke value
            if cursor.description is not None:
                columns = [col[0] for col in cursor.description]
                transaction_dict = dict(zip(columns, transaction))
            else:
                transaction_dict = {}

        cursor.execute("SELECT product_id, quantity, price FROM transaction_items WHERE transaction_id = %s", (id,))
        items = cursor.fetchall()
        if items and not isinstance(items[0], dict):
            if cursor.description:
                item_columns = [col[0] for col in cursor.description]
                items_list = [dict_keys_to_str(dict(zip(item_columns, row))) for row in items]
            else:
                items_list = []
        else:
            items_list = [dict_keys_to_str(item) for item in items]

        # Buat response dict baru agar linter tidak error
        response_dict = {}
        for k in transaction_dict:
            response_dict[str(k)] = transaction_dict[k]
        response_dict['items'] = items_list  # type: ignore

        cursor.close()
        conn.close()
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch transaction by ID'}), 500
