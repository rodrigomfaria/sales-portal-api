# Sales Portal API

API desenvolvida com FastAPI para portal de vendas.

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

A API estará disponível em: http://localhost:8000

### Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura do Projeto

```
sales-portal-api/
├── main.py              # Arquivo principal da API
├── Pipfile             # Dependências do projeto
├── Pipfile.lock        # Lock das versões das dependências
└── app/                # Pacote principal da aplicação
    ├── __init__.py
    ├── models/         # Modelos de dados
    ├── routers/        # Rotas da API
    └── services/       # Lógica de negócio
```

## Comandos Úteis

- `pipenv install <package>` - Instalar nova dependência
- `pipenv install --dev <package>` - Instalar dependência de desenvolvimento
- `pipenv shell` - Ativar ambiente virtual
- `pipenv run <command>` - Executar comando no ambiente virtual
- `pipenv graph` - Ver árvore de dependências
