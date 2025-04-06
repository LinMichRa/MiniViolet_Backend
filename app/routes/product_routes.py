#CREAR PRODUCTO (condicion rol admin)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.models import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'precio': float(p.precio),
        'categoria': p.categoria,
        'imagen_url': p.imagen_url,
        'stock': p.stock
    } for p in products])

@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    user = get_jwt_identity()
    if user['rol'] != 'admin':
        return jsonify({'msg': 'Solo administradores pueden crear productos'}), 403

    data = request.json
    product = Product(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=data['precio'],
        categoria=data['categoria'],
        imagen_url=data.get('imagen_url'),
        stock=data['stock'],
        created_by=user['id']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'msg': 'Producto creado exitosamente'})

@product_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    user = get_jwt_identity()
    if user['rol'] != 'admin':
        return jsonify({'msg': 'No autorizado'}), 403

    product = Product.query.get_or_404(id)
    data = request.json
    for field in ['nombre', 'descripcion', 'precio', 'categoria', 'imagen_url', 'stock']:
        if field in data:
            setattr(product, field, data[field])
    db.session.commit()
    return jsonify({'msg': 'Producto actualizado'})

@product_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    user = get_jwt_identity()
    if user['rol'] != 'admin':
        return jsonify({'msg': 'No autorizado'}), 403
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'msg': 'Producto eliminado'})

