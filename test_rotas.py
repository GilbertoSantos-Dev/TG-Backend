import requests

# Substitua pela URL do seu servidor
base_url = 'http://localhost:5000'

def test_get_rotas():
    response = requests.get(f'{base_url}/rotas')
    print(response.status_code, response.json())

def test_create_rota():
    rota_data = {
        'descricao': 'Nova Rota'
    }
    response = requests.post(f'{base_url}/rotas', json=rota_data)
    print(response.status_code, response.json())

def test_get_rota(id):
    response = requests.get(f'{base_url}/rotas/{id}')
    print(response.status_code, response.json())

# Testar rotas
test_get_rotas()
test_create_rota()
test_get_rota(1)  # Substitua pelo ID que você sabe que existe
