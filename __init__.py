from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_jwt_extended import JWTManager

mysql = MySQL()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app)
    mysql.init_app(app)
    jwt.init_app(app)

    from app.routes import auth, product, cart, transaction
    app.register_blueprint(auth.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(transaction.bp)

    return app
