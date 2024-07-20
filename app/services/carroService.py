from app import db
from app.models import Carro

class CarroService:
    @staticmethod
    def create_carro(data):
        modelo = data.get('modelo')
        ano = data.get('ano')
        placa = data.get('placa')
        km = data.get('km')

        new_carro = Carro(modelo=modelo, ano=ano, placa=placa, km=km)
        db.session.add(new_carro)
        db.session.commit()

        return new_carro.to_dict()

    @staticmethod
    def get_all_carros():
        carros = Carro.query.all()
        return [carro.to_dict() for carro in carros]

    @staticmethod
    def get_carro_by_id(id):
        carro = Carro.query.get(id)
        return carro.to_dict() if carro else None

    @staticmethod
    def update_carro(id, data):
        carro = Carro.query.get(id)
        if carro:
            carro.modelo = data.get('modelo', carro.modelo)
            carro.ano = data.get('ano', carro.ano)
            carro.placa = data.get('placa', carro.placa)
            carro.km = data.get('km', carro.km)
            db.session.commit()
            return carro.to_dict()
        return None

    @staticmethod
    def delete_carro(id):
        carro = Carro.query.get(id)
        if carro:
            db.session.delete(carro)
            db.session.commit()
            return True
        return False

carroService = CarroService()
