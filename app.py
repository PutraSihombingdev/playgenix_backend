from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from routes.auth import auth
from routes.product import product
from routes.cart import cart
from routes.payment import payment
from routes.transaction import transaction
from routes.review import review

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(cart)
app.register_blueprint(payment)
app.register_blueprint(transaction)
app.register_blueprint(review)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Backend is running', 'timestamp': '2024-01-01T00:00:00Z'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting PlayGenix Backend...")
    print("📍 Server will run at: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/api/health")
    print("📝 API Documentation: Check README.md")
    app.run(debug=True, host='0.0.0.0', port=5000)