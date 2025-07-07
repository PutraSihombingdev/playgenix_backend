from flask import Blueprint, request, jsonify, g
from db import get_connection
from utils.jwt_helper import generate_token, jwt_required
import hashlib
import mysql.connector

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if not username or not password or not email:
            return jsonify({'error': 'Username, email, dan password wajib diisi'}), 400

        conn = get_connection()
        cursor = conn.cursor()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Register sukses'}), 201
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({'error': 'Username atau email sudah terdaftar'}), 409
        return jsonify({'error': 'Kesalahan database'}), 500
    except Exception as e:
        print(f"Register error: {e}")
        return jsonify({'error': 'Terjadi kesalahan di server'}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({'error': 'Username dan password wajib diisi'}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, hashed_pw)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and isinstance(user, dict) and "id" in user and "username" in user:
            token_data = {
                "user_id": user["id"],
                "username": user["username"]
            }
            token = generate_token(token_data)
            return jsonify({
                "token": token,
                "user": {
                    "id": user["id"],
                    "username": user["username"]
                }
            }), 200
        else:
            print("DEBUG user value:", user)
            return jsonify({"error": "Username atau password salah"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Terjadi kesalahan di server'}), 500