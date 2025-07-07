import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify, g

load_dotenv()

def generate_token(data):
    secret_key = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    return jwt.encode({
        **data,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }, secret_key, algorithm="HS256")

def decode_token(token):
    try:
        secret_key = os.getenv("JWT_SECRET_KEY", "jwtsecret")
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization']
            if bearer.startswith('Bearer '):
                token = bearer[7:]
        if not token:
            return jsonify({'error': 'Token tidak ditemukan'}), 401
        try:
            secret = os.getenv('JWT_SECRET_KEY', 'jwtsecret')
            data = jwt.decode(token, secret, algorithms=["HS256"])
            g.user = data
        except Exception as e:
            return jsonify({'error': 'Token tidak valid'}), 401
        return f(*args, **kwargs)
    return decorated
