from app.models import Atividade, Usuario, db

class AtividadeService:
    @staticmethod
    def create_atividade(data):
        try:
            atividade = Atividade(
                dist_percorrida=data.get('dist_percorrida'),
                rota_id=data.get('rota_id'),
                local_id=data.get('local_id'),
                carro_id=data.get('carro_id'),
                km_inicial=data.get('km_inicial'),
                km_final=data.get('km_final'),
                hora_inicio=data.get('hora_inicio'),
                hora_fim=data.get('hora_fim'),
                data=data.get('data')
            )
            usuarios_ids = data.get('usuarios', [])
            usuarios = Usuario.query.filter(Usuario.id.in_(usuarios_ids)).all()
            atividade.usuarios = usuarios

            db.session.add(atividade)
            db.session.commit()
            return atividade.to_dict()
        except Exception as e:
            print(f"Erro ao criar atividade: {e}")
            return None

    @staticmethod
    def get_all_atividades():
        atividades = Atividade.query.all()
        return [atividade.to_dict() for atividade in atividades]

    @staticmethod
    def get_atividade_by_id(id):
        atividade = Atividade.query.get(id)
        if atividade:
            return atividade.to_dict()
        return None

    @staticmethod
    def update_atividade(id, data):
        atividade = Atividade.query.get(id)
        if atividade:
            atividade.dist_percorrida = data.get('dist_percorrida', atividade.dist_percorrida)
            atividade.rota_id = data.get('rota_id', atividade.rota_id)
            atividade.local_id = data.get('local_id', atividade.local_id)
            atividade.carro_id = data.get('carro_id', atividade.carro_id)
            atividade.km_inicial = data.get('km_inicial', atividade.km_inicial)
            atividade.km_final = data.get('km_final', atividade.km_final)
            atividade.hora_inicio = data.get('hora_inicio', atividade.hora_inicio)
            atividade.hora_fim = data.get('hora_fim', atividade.hora_fim)
            atividade.data = data.get('data', atividade.data)

            usuarios_ids = data.get('usuarios', [])
            if usuarios_ids:
                usuarios = Usuario.query.filter(Usuario.id.in_(usuarios_ids)).all()
                atividade.usuarios = usuarios

            db.session.commit()
            return atividade.to_dict()
        return None

    @staticmethod
    def delete_atividade(id):
        atividade = Atividade.query.get(id)
        if atividade:
            db.session.delete(atividade)
            db.session.commit()
            return True
        return False
