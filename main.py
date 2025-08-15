import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging para debug
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Criar instância do FastAPI
app = FastAPI(
    title="Sales Portal API",
    description="API para portal de vendas",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz
@app.get("/")
async def read_root():
    logger.debug("Endpoint root acessado")
    return {"message": "Bem-vindo à Sales Portal API!"}

# Rota de health check
@app.get("/health")
async def health_check():
    logger.debug("Health check acessado")
    return {"status": "healthy", "debug": os.getenv("DEBUG", "false")}

# Exemplo de rota com parâmetros
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    logger.debug(f"Item endpoint acessado com item_id={item_id}, q={q}")
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    
    # Configurações para desenvolvimento
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Iniciando servidor em modo debug: {debug_mode}")
    
    try:
        uvicorn.run(
            "main:app",  # Usando string ao invés do objeto app diretamente
            host="0.0.0.0", 
            port=8001,  # Mudando para porta 8001 para evitar conflitos
            reload=debug_mode,
            log_level="debug" if debug_mode else "info"
        )
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")
        raise
