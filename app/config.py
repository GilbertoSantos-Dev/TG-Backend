# app/config.py

import os

class Config:
    # Outras configurações
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  # Chave secreta para JWT
    JWT_TOKEN_LOCATION = ['headers']  # Local onde o token é esperado (no cabeçalho)
