from flask import Blueprint, request, jsonify
from app.services.atividadeService import AtividadeService

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()  # Captura os dados da solicitação
    print("Dados recebidos:", data)
    print("Cabeçalhos recebidos:", request.headers)
    new_atividade = AtividadeService.create_atividade(data)
    if new_atividade:
        return jsonify(new_atividade), 201
    return jsonify({"message": "Erro ao criar atividade"}), 400

@atividade_bp.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = AtividadeService.get_all_atividades()
    return jsonify(atividades), 200

@atividade_bp.route('/atividades/<int:id>', methods=['GET'])
def get_atividade(id):
    atividade = AtividadeService.get_atividade_by_id(id)
    if atividade:
        return jsonify(atividade), 200
    return jsonify({"message": "Atividade not found"}), 404

@atividade_bp.route('/atividades/<int:id>', methods=['PUT'])
def update_atividade(id):
    data = request.get_json()
    updated_atividade = AtividadeService.update_atividade(id, data)
    if updated_atividade:
        return jsonify(updated_atividade), 200
    return jsonify({"message": "Atividade não encontrada"}), 404

@atividade_bp.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
    result = AtividadeService.delete_atividade(id)
    if result:
        return jsonify({"message": "Atividade deletada"}), 200
    return jsonify({"message": "Atividade não encontrada"}), 404
