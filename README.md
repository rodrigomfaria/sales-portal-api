# Sales Portal API

API desenvolvida com FastAPI para portal de vendas, utiliz### 📚 Documentação
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 🗄️ Banco de Dados

O projeto usa **SQLite** (`sales_portal.db`) com **Alembic** para controle de migrações.

### 🔄 Migrações (Alembic)

#### Comandos básicos:
```bash
# Aplicar migrações
alembic upgrade head

# Criar nova migração (automática)
alembic revision --autogenerate -m "Descrição"

# Criar migração manual
alembic revision -m "Descrição"

# Reverter última migração
alembic downgrade -1

# Ver histórico
alembic history

# Ver status atual
alembic current
```

#### Script de gerenciamento:
```bash
python migrations.py
```

### Inicializar manualmente:
```bash
python app/init_db.py
```

### Testar API:

#### Teste manual (demonstração):
```bash
python test/test_sqlite.py
```

#### Testes unitários:
```bash
# Todos os testes
python test/run_tests.py

# Testes específicos
python test/test_models.py    # Testes dos modelos
python test/test_api.py       # Testes das APIs
```

## Estrutura do ProjetoSQLite como banco de dados.

## 🚀 Funcionalidades

- ✅ **FastAPI** - Framework web moderno e rápido
- ✅ **SQLite** - Banco de dados embutido, zero configuração
- ✅ **SQLAlchemy** - ORM para Python
- ✅ **Pydantic** - Validação de dados
- ✅ **Swagger/OpenAPI** - Documentação automática
- ✅ **CORS** - Configurado para desenvolvimento

## 📊 Modelos de Dados

### Usuários (users)
- `id` - Identificador único
- `name` - Nome do usuário
- `email` - Email único
- `is_active` - Status ativo/inativo
- `created_at/updated_at` - Timestamps

### Produtos (products)
- `id` - Identificador único
- `name` - Nome do produto
- `description` - Descrição
- `price` - Preço
- `stock_quantity` - Quantidade em estoque
- `is_active` - Status ativo/inativo

### Vendas (sales)
- `id` - Identificador único
- `user_id` - ID do usuário
- `product_id` - ID do produto
- `quantity` - Quantidade vendida
- `unit_price/total_price` - Preços
- `sale_date` - Data da venda

## Configuração do Ambiente

### Pré-requisitos
- Python 3.13+ (gerenciado via pyenv)
- pipenv

### Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pipenv install
```

3. Ative o ambiente virtual:
```bash
pipenv shell
```

4. Execute a aplicação:
```bash
python main.py
```

Ou usando pipenv:
```bash
pipenv run python main.py
```

## Uso

A API estará disponível em: http://localhost:8001

### 🔗 Endpoints Principais

#### Usuários
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Obter usuário por ID
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

### 📚 Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
sales-portal-api/
├── main.py              # Arquivo principal da API
├── sales_portal.db      # Banco de dados SQLite
├── migrations.py        # Gerenciador de migrações
├── alembic.ini          # Configuração do Alembic
├── Pipfile             # Dependências do projeto
├── Pipfile.lock        # Lock das versões das dependências
├── alembic/            # Pasta de migrações
│   ├── env.py          # Configuração do ambiente
│   └── versions/       # Arquivos de migração
├── test/               # Pasta de testes
│   ├── __init__.py     # Inicializador do pacote
│   ├── run_tests.py    # Executar todos os testes
│   ├── test_api.py     # Testes de integração das APIs
│   ├── test_models.py  # Testes unitários dos modelos
│   └── test_sqlite.py  # Teste manual/demonstração
└── app/                # Pacote principal da aplicação
    ├── __init__.py
    ├── database.py     # Configuração do banco
    ├── schemas.py      # Schemas Pydantic
    ├── init_db.py      # Inicializador do banco
    ├── models/         # Modelos SQLAlchemy
    │   └── __init__.py # User, Product, Sale
    ├── routers/        # Rotas da API
    │   ├── __init__.py
    │   └── users.py    # CRUD de usuários
    └── services/       # Lógica de negócio
```

## Comandos Úteis

- `pipenv install <package>` - Instalar nova dependência
- `pipenv install --dev <package>` - Instalar dependência de desenvolvimento
- `pipenv shell` - Ativar ambiente virtual
- `pipenv run <command>` - Executar comando no ambiente virtual
- `pipenv graph` - Ver árvore de dependências
