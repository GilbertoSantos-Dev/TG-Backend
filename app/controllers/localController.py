from flask import Blueprint, request, jsonify
from app.services.localService import localService  # Importa a instância de localService

local_bp = Blueprint('local_bp', __name__)

@local_bp.route('/locais', methods=['POST'])
def create_local():
    try:
        data = request.get_json()
        new_local = localService.create_local(data)
        return jsonify(new_local), 201
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@local_bp.route('/locais', methods=['GET'])
def get_locais():
    locais = localService.get_all_locais()
    return jsonify(locais), 200

@local_bp.route('/locais/<int:id>', methods=['GET'])
def get_local(id):
    local = localService.get_local_by_id(id)  # Utiliza localService, não LocalService
    if local:
        return jsonify(local), 200
    return jsonify({"message": "Local not found"}), 404

@local_bp.route('/locais/<int:id>', methods=['PUT'])
def update_local(id):
    data = request.get_json()
    updated_local = localService.update_local(id, data)
    if updated_local:
        return jsonify(updated_local), 200
    return jsonify({"message": "Local not found"}), 404

@local_bp.route('/locais/<int:id>', methods=['DELETE'])
def delete_local(id):
    result = localService.delete_local(id)
    if result:
        return jsonify({"message": "Local deleted"}), 200
    return jsonify({"message": "Local not found"}), 404
