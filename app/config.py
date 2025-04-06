import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
