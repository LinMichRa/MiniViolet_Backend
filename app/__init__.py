from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from .config import Config
from dotenv import load_dotenv
import os

# Extensiones
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Registro de Blueprints
    from .routes.auth_routes import auth_bp
    #from .routes.product_routes import product_bp
    #from .routes.cart_routes import cart_bp
    #from .routes.order_routes import order_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    #app.register_blueprint(product_bp, url_prefix='/api/products')
    #app.register_blueprint(cart_bp, url_prefix='/api/cart')
    #app.register_blueprint(order_bp, url_prefix='/api/orders')

    return app