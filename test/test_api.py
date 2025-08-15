"""
Testes de integração para APIs
"""
import unittest
import requests
import sys
import os
import time

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAPI(unittest.TestCase):
    """
    Testes para as APIs REST
    """
    
    BASE_URL = "http://localhost:8001"
    
    @classmethod
    def setUpClass(cls):
        """Verificar se API está rodando"""
        try:
            response = requests.get(f"{cls.BASE_URL}/health", timeout=5)
            if response.status_code != 200:
                raise Exception("API não está respondendo")
        except requests.exceptions.RequestException:
            raise unittest.SkipTest("API não está rodando. Execute: python main.py")
    
    def test_root_endpoint(self):
        """Testar endpoint raiz"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        
    def test_health_check(self):
        """Testar health check"""
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        
    def test_create_user(self):
        """Testar criação de usuário"""
        user_data = {
            "name": "Test User API",
            "email": f"test_api_{int(time.time())}@example.com"  # Email único
        }
        
        response = requests.post(f"{self.BASE_URL}/api/v1/users/", json=user_data)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["name"], user_data["name"])
        self.assertEqual(data["email"], user_data["email"])
        self.assertTrue(data["is_active"])
        self.assertIn("id", data)
        
    def test_list_users(self):
        """Testar listagem de usuários"""
        response = requests.get(f"{self.BASE_URL}/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIsInstance(data, list)
        
    def test_get_nonexistent_user(self):
        """Testar busca de usuário inexistente"""
        response = requests.get(f"{self.BASE_URL}/api/v1/users/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
