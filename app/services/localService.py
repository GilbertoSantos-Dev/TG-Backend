from app import db
from app.models.models import Local

class LocalService:
    @staticmethod
    def create_local(data):
        descricao = data.get('descricao')
        endereco = data.get('endereco')
        rota_id = data.get('rota_id')
        
        new_local = Local(descricao=descricao, endereco=endereco, rota_id=rota_id)
        db.session.add(new_local)
        db.session.commit()
        
        return new_local.to_dict()  # Retornando um dicionário

    @staticmethod
    def get_all_locais():
        locais = Local.query.all()
        return [local.to_dict() for local in locais]

    @staticmethod
    def get_local_by_id(id):
        local = Local.query.get(id)
        if local:
            return local.to_dict()
        return None

    @staticmethod
    def update_local(id, data):
        local = Local.query.get(id)
        if local:
            local.descricao = data.get('descricao', local.descricao)
            local.endereco = data.get('endereco', local.endereco)
            local.rota_id = data.get('rota_id', local.rota_id)
            db.session.commit()
            return local.to_dict()
        return None

    @staticmethod
    def delete_local(id):
        local = Local.query.get(id)
        if local:
            db.session.delete(local)
            db.session.commit()
            return True
        return False

localService = LocalService()
