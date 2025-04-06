from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .. import db
from ..models.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': 'Usuario ya existe'}), 400

    user = User(
        nombre=data['nombre'],
        apellido=data['apellido'],
        tipo_identificacion=data['tipo_identificacion'],
        identificacion=data['identificacion'],
        fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d'),
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        rol=data.get('rol', 'user')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Usuario registrado exitosamente'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'msg': 'Credenciales inválidas'}), 401

    token = create_access_token(identity={'id': user.id, 'rol': user.rol.value})
    return jsonify({'token': token})