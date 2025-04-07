#CREAR PRODUCTO (condicion rol admin)
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from .. import db
from ..models.models import Category, Product
from ..utils.s3_helper import subir_a_s3
from ..utils.s3_upload import subir_a_s3
from dotenv import load_dotenv

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
    load_dotenv()

    if request.method == "OPTIONS":
        return jsonify({"msg": "CORS preflight OK"}), 200

    user_id = get_jwt_identity()
    claims = get_jwt()
    rol = claims.get("rol")

    if rol != 'admin':
        return jsonify({'msg': 'Solo administradores pueden crear productos'}), 403

    try:
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion')
        precio = float(request.form['precio'])
        categoria_nombre = request.form['categoria'].strip().lower()  # Normaliza
        stock = int(request.form['stock'])
        file = request.files.get('imagen')

        # Buscar o crear la categoría
        categoria = Category.query.filter_by(nombre=categoria_nombre).first()
        if not categoria:
            categoria = Category(nombre=categoria_nombre)
            db.session.add(categoria)
            db.session.flush()  # Para obtener el ID sin hacer commit aún

        imagen_url = subir_a_s3(file, folder='productos') if file else None

        product = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria.nombre,  # Guarda el nombre en el producto
            imagen_url=imagen_url,
            stock=stock,
            created_by=user_id
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({
            'msg': 'Producto creado exitosamente',
            'producto': {
                'id': product.id,
                'nombre': product.nombre,
                'imagen_url': product.imagen_url
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Error al crear el producto', 'error': str(e)}), 500


@product_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({'msg': 'No autorizado'}), 403

    producto = Product.query.get_or_404(id)

    producto.nombre = request.form.get('nombre')
    producto.descripcion = request.form.get('descripcion')
    producto.precio = request.form.get('precio')
    producto.categoria = request.form.get('categoria')
    producto.stock = request.form.get('stock')

    imagen = request.files.get('imagen')
    if imagen:
        imagen_url = subir_a_s3(imagen, folder='productos')
        producto.imagen_url = imagen_url

    db.session.commit()
    return jsonify({'msg': 'Producto actualizado correctamente'})

@product_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({'msg': 'No autorizado'}), 403
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'msg': 'Producto eliminado'})

