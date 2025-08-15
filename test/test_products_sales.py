"""
Script de teste para produtos e vendas
"""
import requests
import json
from datetime import date


def test_products_and_sales():
    """
    Testar APIs de produtos e vendas
    """
    base_url = "http://localhost:8001"
    
    print("🚀 Testando APIs de Produtos e Vendas...")
    print("=" * 60)
    
    # Verificar se API está funcionando
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ API Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando. Execute: python main.py")
        return
    
    # 1. Criar usuário primeiro
    print("\n👤 Criando usuário...")
    user_data = {
        "name": "João Vendedor",
        "email": "joao.vendedor@email.com"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/users/", json=user_data)
        if response.status_code == 200:
            user = response.json()
            user_id = user['id']
            print(f"✅ Usuário criado: ID {user_id}")
        else:
            print(f"❌ Erro ao criar usuário: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # 2. Criar produtos
    print("\n📦 Criando produtos...")
    products_data = [
        {
            "name": "Notebook Dell",
            "description": "Notebook Dell Inspiron 15",
            "price": 2500.00,
            "stock_quantity": 10
        },
        {
            "name": "Mouse Wireless",
            "description": "Mouse sem fio USB",
            "price": 45.90,
            "stock_quantity": 50
        },
        {
            "name": "Teclado Mecânico",
            "description": "Teclado mecânico RGB",
            "price": 299.90,
            "stock_quantity": 0  # Sem estoque
        }
    ]
    
    product_ids = []
    for product_data in products_data:
        try:
            response = requests.post(f"{base_url}/api/v1/products/", json=product_data)
            if response.status_code == 200:
                product = response.json()
                product_ids.append(product['id'])
                print(f"✅ Produto criado: {product['name']} (ID: {product['id']})")
            else:
                print(f"❌ Erro ao criar produto: {response.text}")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # 3. Listar produtos
    print("\n📋 Listando produtos...")
    try:
        response = requests.get(f"{base_url}/api/v1/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ {len(products)} produto(s) encontrado(s)")
            for product in products:
                print(f"   - {product['name']}: R$ {product['price']:.2f} (Estoque: {product['stock_quantity']})")
        else:
            print(f"❌ Erro ao listar produtos: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 4. Buscar produtos em estoque
    print("\n🔍 Produtos em estoque...")
    try:
        response = requests.get(f"{base_url}/api/v1/products/in-stock")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ {len(products)} produto(s) em estoque")
            for product in products:
                print(f"   - {product['name']}: {product['stock_quantity']} unidades")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Criar vendas
    print("\n💰 Criando vendas...")
    if len(product_ids) >= 2:
        sales_data = [
            {
                "user_id": user_id,
                "product_id": product_ids[0],  # Notebook
                "quantity": 1
            },
            {
                "user_id": user_id,
                "product_id": product_ids[1],  # Mouse
                "quantity": 3
            }
        ]
        
        for sale_data in sales_data:
            try:
                response = requests.post(f"{base_url}/api/v1/sales/", json=sale_data)
                if response.status_code == 200:
                    sale = response.json()
                    print(f"✅ Venda criada: ID {sale['id']}, Total: R$ {sale['total_price']:.2f}")
                else:
                    print(f"❌ Erro ao criar venda: {response.text}")
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    # 6. Tentar venda sem estoque
    print("\n⚠️ Testando venda sem estoque...")
    if len(product_ids) >= 3:
        try:
            response = requests.post(f"{base_url}/api/v1/sales/", json={
                "user_id": user_id,
                "product_id": product_ids[2],  # Teclado sem estoque
                "quantity": 1
            })
            if response.status_code != 200:
                print(f"✅ Erro esperado: {response.json()['detail']}")
            else:
                print("❌ Deveria ter dado erro de estoque!")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # 7. Resumo de vendas
    print("\n📊 Resumo de vendas...")
    try:
        response = requests.get(f"{base_url}/api/v1/sales/summary")
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Resumo de vendas:")
            print(f"   - Total de vendas: {summary['summary']['total_sales']}")
            print(f"   - Valor total: R$ {summary['summary']['total_value']:.2f}")
            print(f"   - Quantidade total: {summary['summary']['total_quantity']}")
            print(f"   - Valor médio por venda: R$ {summary['summary']['average_sale_value']:.2f}")
        else:
            print(f"❌ Erro ao obter resumo: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 8. Vendas de hoje
    print("\n📅 Vendas de hoje...")
    try:
        response = requests.get(f"{base_url}/api/v1/sales/today")
        if response.status_code == 200:
            sales = response.json()
            print(f"✅ {len(sales)} venda(s) hoje")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print(f"\n🎉 Teste concluído!")
    print(f"📚 Documentação: {base_url}/docs")


if __name__ == "__main__":
    test_products_and_sales()
