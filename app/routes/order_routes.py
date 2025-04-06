import stripe
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.models import CartItem, Product, Order, OrderItem, PaymentLog
from flask import current_app
from dotenv import load_dotenv

order_bp = Blueprint('orders', __name__)
load_dotenv()

#IMPLEMENTACION FUNCIONES ORDENES
@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = int(get_jwt_identity())
    items = CartItem.query.filter_by(user_id=user_id).all()
    if not items:
        return jsonify({'msg': 'Carrito vacío'}), 400

    total = 0
    for item in items:
        product = Product.query.get(item.product_id)
        if not product or product.stock < item.cantidad:
            return jsonify({'msg': f"Producto no disponible o sin stock: {item.product_id}"}), 400
        total += float(product.precio) * item.cantidad

    order = Order(user_id=user_id, total=total, status='pendiente')
    db.session.add(order)
    db.session.flush()

    for item in items:
        product = Product.query.get(item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            cantidad=item.cantidad,
            precio_unit=product.precio
        )
        db.session.add(order_item)
        product.stock -= item.cantidad
        db.session.delete(item)

    db.session.commit()


    # IMPLEMENTACION STRIPE
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        charge = stripe.Charge.create(
            amount=int(total * 100),  # en centavos por cuenta Stripe :p
            currency='usd',
            description=f"Orden {order.id}",
            source='tok_visa'
        )
        order.status = 'pagado'
        resultado = 'exito'
    except stripe.error.StripeError as e:
        resultado = 'error'
        order.status = 'fallido'
        charge = {'error': str(e.user_message) if hasattr(e, 'user_message') else str(e)}

    db.session.add(PaymentLog(
        user_id=user_id,
        order_id=order.id,
        resultado=resultado,
        detalle=charge
    ))
    db.session.commit()

    return jsonify({'msg': 'Orden procesada', 'estado': order.status})
