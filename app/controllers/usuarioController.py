from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario
from app import db, bcrypt
from app.services.usuarioService import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nome = data.get('nome')
    user_name = data.get('user_name')
    senha = data.get('senha')
    papel = data.get('papel')

    senha_hash = generate_password_hash(senha)

    novo_usuario = Usuario(nome=nome, user_name=user_name, senha_hash=senha_hash, papel=papel)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(novo_usuario.to_dict(include_senha_hash=False)), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = UsuarioService.get_all_usuarios()
    return jsonify(usuarios), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = UsuarioService.get_usuario_by_id(id)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({"message": "Usuario não encontrado"}), 404

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    updated_usuario = UsuarioService.update_usuario(id, data)
    if updated_usuario:
        return jsonify(updated_usuario), 200
    return jsonify({"message": "Usuario não encontrado"}), 404

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    print(f"Deleting user with ID: {id}")
    result = UsuarioService.delete_usuario(id)
    if result:
        return jsonify({"message": "Usuario deletado"}), 200
    return jsonify({"message": "Usuario não encontrado"}), 404

@jwt_required()
@usuario_bp.route('/usuarios/UsuarioAtivo/change-password', methods=['PUT'])
def change_password():
    data = request.get_json()
    print("Headers recebidos:", request.headers)  # Log dos headers recebidos
    print("Dados recebidos:", data)  # Log detalhado dos dados recebidos
    
    if not data:
        print("Erro: Nenhum dado recebido")
        return jsonify({'error': 'Nenhum dado recebido'}), 422

    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    
    # Log dos dados individuais recebidos
    print("Senha atual:", current_password)
    print("Nova senha:", new_password)
    print("Confirmação da nova senha:", confirm_new_password)
    
    # Verificação dos dados recebidos
    if not current_password or not new_password or not confirm_new_password:
        print("Erro: Campos obrigatórios ausentes")
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 422

    if new_password != confirm_new_password:
        print("Erro: Novas senhas não coincidem")
        return jsonify({'error': 'As novas senhas não coincidem'}), 422

    # Continue com a lógica de troca de senha
    # Aqui você pode adicionar a lógica para verificar a senha atual e atualizar a senha

    return jsonify({'message': 'Senha alterada com sucesso'}), 200
