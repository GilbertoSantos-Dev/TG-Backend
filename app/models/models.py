from app import db
from werkzeug.security import generate_password_hash, check_password_hash

usuario_atividade_association = db.Table('usuario_atividade_association',
                                         db.Column('usuario_id', db.Integer, db.ForeignKey(
                                             'usuario.id'), primary_key=True),
                                         db.Column('atividade_id', db.Integer, db.ForeignKey(
                                             'atividade.id'), primary_key=True)
                                         )


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    papel = db.Column(db.String(20), nullable=False)
    atividades = db.relationship(
        'Atividade', secondary=usuario_atividade_association, back_populates='usuarios')

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self, include_senha_hash=True):
        user_dict = {
            'id': self.id,
            'nome': self.nome,
            'user_name': self.user_name,
            'papel': self.papel
        }
        if include_senha_hash:
            user_dict['senha_hash'] = self.senha_hash
        return user_dict

class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(50), nullable=False)
    km = db.Column(db.Float, nullable=False)
    atividades = db.relationship('Atividade', back_populates='carro')

    def to_dict(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'ano': self.ano,
            'placa': self.placa,
            'km': self.km
        }


class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    locais = db.relationship(
        'Local', back_populates='rota', cascade='all, delete-orphan')
    atividades = db.relationship('Atividade', back_populates='rota')

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao
        }


class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    rota_id = db.Column(db.Integer, db.ForeignKey('rota.id'), nullable=False)
    rota = db.relationship('Rota', back_populates='locais')
    atividades = db.relationship('Atividade', back_populates='local')

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'endereco': self.endereco,
            'rota': self.rota.to_dict() if self.rota else None
        }


class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dist_percorrida = db.Column(db.Float, nullable=False)
    rota_id = db.Column(db.Integer, db.ForeignKey('rota.id'), nullable=False)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)
    carro_id = db.Column(db.Integer, db.ForeignKey('carro.id'), nullable=False)
    km_inicial = db.Column(db.Float, nullable=False)
    km_final = db.Column(db.Float, nullable=False)
    hora_inicio = db.Column(db.DateTime, nullable=False)
    hora_fim = db.Column(db.DateTime, nullable=False)
    data = db.Column(db.Date, nullable=False)

    rota = db.relationship('Rota', back_populates='atividades')
    local = db.relationship('Local', back_populates='atividades')
    carro = db.relationship('Carro', back_populates='atividades')
    usuarios = db.relationship(
        'Usuario', secondary=usuario_atividade_association, back_populates='atividades')

    def calcular_distancia(self):
        return self.km_final - self.km_inicial

    def calcular_duracao(self):
        return self.hora_fim - self.hora_inicio

    def to_dict(self):
        return {
            'id': self.id,
            'dist_percorrida': self.dist_percorrida,
            'rota': self.rota.to_dict() if self.rota else None,
            'local': self.local.to_dict() if self.local else None,
            'carro': self.carro.to_dict() if self.carro else None,
            'km_inicial': self.km_inicial,
            'km_final': self.km_final,
            'hora_inicio': self.hora_inicio,
            'hora_fim': self.hora_fim,
            'data': self.data,
            'usuarios': [usuario.to_dict() for usuario in self.usuarios]
        }
