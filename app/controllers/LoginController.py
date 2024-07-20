from flask import Blueprint, request, jsonify
import jwt
import datetime
from app.models import Usuario

login_bp = Blueprint('login_bp', __name__)

SECRET_KEY = 'sua_chave_secreta_aqui'

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    senha = data.get('senha')

    user = Usuario.query.filter_by(user_name=user_name).first()
    
    if user and user.check_senha(senha):
        # Gerar o token de sessão
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        
        # Retornar o token e o papel do usuário na resposta
        return jsonify({
            'token': token,
            'papel': user.papel
        })
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401
