from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.models import CartItem, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def view_cart():
    user_id = get_jwt_identity()['id']
    items = CartItem.query.filter_by(user_id=user_id).all()
    result = []
    for item in items:
        product = Product.query.get(item.product_id)
        result.append({
            'product_id': product.id,
            'nombre': product.nombre,
            'precio': float(product.precio),
            'cantidad': item.cantidad
        })
    return jsonify(result)

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()['id']
    data = request.json
    item = CartItem.query.filter_by(user_id=user_id, product_id=data['product_id']).first()
    if item:
        item.cantidad += data['cantidad']
    else:
        item = CartItem(user_id=user_id, product_id=data['product_id'], cantidad=data['cantidad'])
        db.session.add(item)
    db.session.commit()
    return jsonify({'msg': 'Producto añadido al carrito'})

@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()['id']
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({'msg': 'Producto eliminado del carrito'})