from flask import Blueprint, request, jsonify
from app.services.rotaService import RotaService

rota_bp = Blueprint('rota_bp', __name__)

@rota_bp.route('/rotas', methods=['POST'])
def create_rota():
    data = request.get_json()
    new_rota = RotaService.create_rota(data)
    return jsonify(new_rota), 201

@rota_bp.route('/rotas', methods=['GET'])
def get_rotas():
    rotas = RotaService.get_all_rotas()
    return jsonify(rotas), 200

@rota_bp.route('/rotas/<int:id>', methods=['GET'])
def get_rota(id):
    rota = RotaService.get_rota_by_id(id)
    if rota:
        return jsonify(rota), 200
    return jsonify({"message": "rota not found"}), 404

@rota_bp.route('/rotas/<int:id>', methods=['PUT'])
def update_rota(id):
    data = request.get_json()
    updated_rota = RotaService.update_rota(id, data)
    if updated_rota:
        return jsonify(updated_rota), 200
    return jsonify({"message": "rota not found"}), 404

@rota_bp.route('/rotas/<int:id>', methods=['DELETE'])
def delete_rota(id):
    result = RotaService.delete_rota(id)
    if result:
        return jsonify({"message": "rota deleted"}), 200
    return jsonify({"message": "rota not found"}), 404
