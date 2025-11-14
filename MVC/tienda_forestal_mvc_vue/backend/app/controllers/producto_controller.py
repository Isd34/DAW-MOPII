from flask import Blueprint, jsonify
from models.producto_model import obtener_productos

producto_blueprint = Blueprint('producto', __name__)

@producto_blueprint.route('/productos', methods=['GET'])
def lista_productos():
    productos = obtener_productos()
    return jsonify(productos)

