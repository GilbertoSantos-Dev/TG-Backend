from app import db
from app.models.models import Rota

class RotaService:
    @staticmethod
    def create_rota(data):
        new_rota = Rota(
            descricao=data.get('descricao')
        )
        db.session.add(new_rota)
        db.session.commit()
        return new_rota.to_dict()

    @staticmethod
    def get_all_rotas():
        rotas = Rota.query.all()
        return [rota.to_dict() for rota in rotas]

    @staticmethod
    def get_rota_by_id(rota_id):
        print (rota_id)
        rota = Rota.query.get(rota_id)
        if rota:
            return rota.to_dict()
        return None

    @staticmethod
    def update_rota(rota_id, data):
        rota = Rota.query.get(rota_id)
        if rota:
            rota.descricao = data.get('descricao', rota.descricao)
            db.session.commit()
            return rota.to_dict()
        return None

    @staticmethod
    def delete_rota(rota_id):
        rota = Rota.query.get(rota_id)
        if rota:
            db.session.delete(rota)
            db.session.commit()
            return True
        return False
