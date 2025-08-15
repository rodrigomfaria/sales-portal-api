"""
Script de teste para demonstrar o funcionamento do SQLite
"""
import requests
import json


def test_api():
    """
    Testar as rotas da API com dados de exemplo
    """
    base_url = "http://localhost:8001"
    
    print("🚀 Testando API com SQLite...")
    
    # 1. Verificar se API está funcionando
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ API Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando. Execute: python main.py")
        return
    
    # 2. Criar usuário
    print("\n📝 Criando usuário...")
    user_data = {
        "name": "João Silva",
        "email": "joao@email.com"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/users/", json=user_data)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuário criado: ID {user['id']}")
            print(f"   Nome: {user['name']}")
            print(f"   Email: {user['email']}")
            print(f"   Criado em: {user['created_at']}")
        else:
            print(f"❌ Erro ao criar usuário: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 3. Listar usuários
    print("\n📋 Listando usuários...")
    try:
        response = requests.get(f"{base_url}/api/v1/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ {len(users)} usuário(s) encontrado(s)")
            for user in users:
                print(f"   - ID: {user['id']}, Nome: {user['name']}, Email: {user['email']}")
        else:
            print(f"❌ Erro ao listar usuários: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 4. Verificar documentação
    print(f"\n📚 Documentação disponível em:")
    print(f"   - Swagger UI: {base_url}/docs")
    print(f"   - ReDoc: {base_url}/redoc")


if __name__ == "__main__":
    test_api()
