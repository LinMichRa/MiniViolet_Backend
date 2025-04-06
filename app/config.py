import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql://usuario:password@localhost/miniviolet")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")