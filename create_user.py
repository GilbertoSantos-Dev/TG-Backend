from app import create_app, db
from flask_bcrypt import Bcrypt
from app.models.usuario import Usuario

app = create_app()
bcrypt = Bcrypt(app)  # Inicialize o Bcrypt com a aplicação

with app.app_context():
    db.create_all()  # Cria todas as tabelas definidas
    
    # Dados do novo usuário
    user_name = "paulo"
    senha = bcrypt.generate_password_hash("123").decode('utf-8')
    
    # Verificar se o usuário já existe
    existing_user = Usuario.query.filter_by(user_name=user_name).first()
    if existing_user:
        print("Usuário já existe!")
    else:
        # Criar um novo usuário
        new_user = Usuario(user_name=user_name, senha=senha)
        db.session.add(new_user)
        db.session.commit()
        print("Usuário criado com sucesso!")
