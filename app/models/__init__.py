from app import db
from .models import Usuario, Carro, Rota, Local, Atividade

# Torne db acessível quando importar o módulo models
__all__ = ['db', 'Usuario', 'Carro', 'Rota', 'Local', 'Atividade']
