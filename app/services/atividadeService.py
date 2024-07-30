from app.models import Atividade, Usuario, db
from app.models.models import Carro, Rota
from datetime import datetime

class AtividadeService:
    @staticmethod
    def create_atividade(data):
        try:
            print(f"Dados recebidos: {data}")
            rota = Rota.query.filter_by(descricao=data['rota']).first()
            if not rota:
                raise ValueError(f"Rota não encontrada: {data['rota']}")
            
            _, placa = data['carro'].split(' - ')
            carro = Carro.query.filter_by(placa=placa).first()
            if not carro:
                raise ValueError(f"Carro não encontrado: {data['carro']}")

            # Certifique-se de que 'local_id' não é nulo
            local_id = data.get('local_id')
            if local_id is None:
                raise ValueError("O campo 'local_id' é obrigatório e não pode ser nulo.")

            data_format = "%d/%m/%Y"
            hora_format = "%H:%M"

            data_str = data.get('data')
            hora_inicio_ts = data.get('hora_inicio')
            hora_fim_ts = data.get('hora_fim')

            # Converter timestamps para strings no formato de hora
            hora_inicio_str = datetime.fromtimestamp(hora_inicio_ts).strftime(hora_format)
            hora_fim_str = datetime.fromtimestamp(hora_fim_ts).strftime(hora_format)

            print(f"Parsing data: {data_str}, hora_inicio: {hora_inicio_str}, hora_fim: {hora_fim_str}")
            
            data_obj = datetime.strptime(data_str, data_format)
            hora_inicio_obj = datetime.strptime(hora_inicio_str, hora_format).time()
            hora_fim_obj = datetime.strptime(hora_fim_str, hora_format).time()

            # Combina a data com a hora
            hora_inicio_datetime = datetime.combine(data_obj, hora_inicio_obj)
            hora_fim_datetime = datetime.combine(data_obj, hora_fim_obj)

            print(f"Data parsed successfully. Data: {data_obj}, Hora início: {hora_inicio_datetime}, Hora fim: {hora_fim_datetime}")
        
            atividade = Atividade(
                dist_percorrida=data.get('dist_percorrida'),
                rota_id=rota.id,
                local_id=local_id,
                carro_id=carro.id,
                km_inicial=data.get('km_inicial'),
                km_final=data.get('km_final'),
                hora_inicio=hora_inicio_datetime,
                hora_fim=hora_fim_datetime,
                data=data_obj
            )

            usuarios_ids = [usuario['id'] for usuario in data.get('equipe', [])]
            usuarios = Usuario.query.filter(Usuario.id.in_(usuarios_ids)).all()
            atividade.usuarios = usuarios

            db.session.add(atividade)
            db.session.commit()
            print("Atividade criada com sucesso")
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
