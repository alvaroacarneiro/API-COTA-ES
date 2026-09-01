from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio
from typing import Optional

app = FastAPI(
    title="API de Cotações (Dólar e Bitcoin)",
    description="API para consultar cotações atualizadas de USD/BRL e BTC/BRL",
    version="1.0.0"
)

# Configuração do CORS (libera para qualquer origem, útil para testes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de resposta para as cotações
class CotacaoModel(BaseModel):
    moeda: str
    nome: str
    compra: float
    venda: float
    variacao_percentual: float
    data_hora: str

class TodasCotacoesModel(BaseModel):
    dolar: Optional[CotacaoModel] = None
    bitcoin: Optional[CotacaoModel] = None
    ultima_atualizacao: str

# URLs da API pública (Awesome API - gratuita e sem chave)
URL_DOLAR = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
URL_BTC = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"

async def buscar_cotacao(url: str, moeda: str, nome: str) -> CotacaoModel:
    """
    Função genérica para buscar cotação em uma URL e retornar o modelo.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()  # Levanta erro se status não for 200
            dados = response.json()
            
            # A Awesome API retorna a chave com o nome da moeda (ex: 'USDBRL')
            chave = moeda.replace("-", "")
            if chave not in dados:
                raise HTTPException(status_code=500, detail=f"Dados inesperados para {moeda}")
            
            cotacao = dados[chave]
            
            return CotacaoModel(
                moeda=moeda,
                nome=nome,
                compra=float(cotacao["bid"]),
                venda=float(cotacao["ask"]),
                variacao_percentual=float(cotacao["pctChange"]),
                data_hora=cotacao["create_date"]
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail=f"Tempo esgotado ao buscar {moeda}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro ao buscar {moeda}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/")
async def raiz():
    """Mensagem de boas-vindas com link para a documentação."""
    return {
        "mensagem": "Bem-vindo à API de Cotações!",
        "documentacao": "/docs",
        "endpoints_disponiveis": [
            "/cotacoes (Dólar + Bitcoin)",
            "/cotacao/usd",
            "/cotacao/btc"
        ]
    }

@app.get("/cotacao/usd", response_model=CotacaoModel)
async def get_dolar():
    """Retorna a cotação atual do Dólar Americano (USD/BRL)."""
    return await buscar_cotacao(URL_DOLAR, "USD-BRL", "Dólar Americano")

@app.get("/cotacao/btc", response_model=CotacaoModel)
async def get_bitcoin():
    """Retorna a cotação atual do Bitcoin (BTC/BRL)."""
    return await buscar_cotacao(URL_BTC, "BTC-BRL", "Bitcoin")

@app.get("/cotacoes", response_model=TodasCotacoesModel)
async def get_todas_cotacoes():
    """
    Retorna as cotações do Dólar e do Bitcoin simultaneamente.
    Ideal para reduzir o tempo de resposta buscando os dados em paralelo.
    """
    try:
        # Executa as duas requisições em paralelo (asyncio.gather)
        dolar_task = buscar_cotacao(URL_DOLAR, "USD-BRL", "Dólar Americano")
        btc_task = buscar_cotacao(URL_BTC, "BTC-BRL", "Bitcoin")
        
        dolar, bitcoin = await asyncio.gather(dolar_task, btc_task)
        
        return TodasCotacoesModel(
            dolar=dolar,
            bitcoin=bitcoin,
            ultima_atualizacao=dolar.data_hora  # Usa a mesma data/hora para ambas
        )
    except HTTPException as e:
        # Se uma das moedas falhar, retornamos parcial com a que deu certo ou erro total
        raise e
