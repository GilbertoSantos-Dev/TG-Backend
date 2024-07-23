from app.models import Usuario, db

class UsuarioService:
    @staticmethod
    def create_usuario(data):
        try:
            new_usuario = Usuario(
                nome=data.get('nome'),
                user_name=data.get('user_name'),
                papel=data.get('papel')
            )
            new_usuario.set_senha(data.get('senha'))
            db.session.add(new_usuario)
            db.session.commit()
            return new_usuario.to_dict(include_senha_hash=False)
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    @staticmethod
    def get_all_usuarios():
        usuarios = Usuario.query.all()
        return [usuario.to_dict(include_senha_hash=False) for usuario in usuarios]

    @staticmethod
    def get_usuario_by_id(id):
        usuario = Usuario.query.get(id)
        if usuario:
            return usuario.to_dict(include_senha_hash=False)
        return None

    @staticmethod
    def update_usuario(id, data):
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                return None
            usuario.nome = data.get('nome', usuario.nome)
            usuario.user_name = data.get('user_name', usuario.user_name)
            usuario.papel = data.get('papel', usuario.papel)
            if 'senha' in data:
                usuario.set_senha(data['senha'])
            db.session.commit()
            return usuario.to_dict(include_senha_hash=False)
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return None

    @staticmethod
    def delete_usuario(id):
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                return None
            db.session.delete(usuario)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return None
