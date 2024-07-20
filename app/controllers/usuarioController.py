from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Usuario
from app import db
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

    return jsonify(novo_usuario.to_dict()), 201

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

@usuario_bp.route('/usuarios/UsuarioAtivo/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()  # Obtém a identidade do usuário do token JWT

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if not current_password or not new_password or not confirm_new_password:
        return jsonify({'message': 'Dados incompletos'}), 400

    if new_password != confirm_new_password:
        return jsonify({'message': 'As novas senhas não coincidem'}), 400

    user = Usuario.query.filter_by(user_name=current_user).first()
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    if not bcrypt.check_password_hash(user.senha, current_password):
        return jsonify({'message': 'Senha atual incorreta'}), 401

    user.senha = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    
    return jsonify({'message': 'Senha alterada com sucesso!'}), 200
