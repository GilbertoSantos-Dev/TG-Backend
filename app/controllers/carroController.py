from flask import Blueprint, request, jsonify
from app.services.carroService import carroService

carro_bp = Blueprint('carro_bp', __name__)

@carro_bp.route('/carros', methods=['POST'])
def create_carro():
    data = request.get_json()
    new_carro = carroService.create_carro(data)
    return jsonify(new_carro), 201

@carro_bp.route('/carros', methods=['GET'])
def get_carros():
    carros = carroService.get_all_carros()
    return jsonify(carros), 200

@carro_bp.route('/carros/<int:id>', methods=['GET'])
def get_carro(id):
    carro = carroService.get_carro_by_id(id)
    if carro:
        return jsonify(carro), 200
    return jsonify({"message": "Carro not found"}), 404

@carro_bp.route('/carros/<int:id>', methods=['PUT'])
def update_carro(id):
    data = request.get_json()
    updated_carro = carroService.update_carro(id, data)
    if updated_carro:
        return jsonify(updated_carro), 200
    return jsonify({"message": "Carro not found"}), 404

@carro_bp.route('/carros/<int:id>', methods=['DELETE'])
def delete_carro(id):
    result = carroService.delete_carro(id)
    if result:
        return jsonify({"message": "Carro deleted"}), 200
    return jsonify({"message": "Carro not found"}), 404
