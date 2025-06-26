import requests
import os

FOSSology_URL = 'http://localhost/api/login'

def authenticate(username, password):

    """
    Função para autenticar no FOSSology e obtem o token de autenticação.
    
    Args:
    - username (str): Nome de usuário.
    - password (str): Senha do usuário.
    
    Returns:
    - str: Token de autenticação se sucesso, None se falha.
    """

    username = os.getenv("FOSSOLOGY_USERNAME", "fossy")  
    password = os.getenv("FOSSOLOGY_PASSWORD", "fossy")  


    payload = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(FOSSology_URL, json=payload)
        
        if response.status_code == 200:
           
            token = response.json().get('token')
            print(f"Autenticação bem-sucedida. Token: {token}")
            return token  
        else:
            print("Falha na autenticação.")
            return None  
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return None  
