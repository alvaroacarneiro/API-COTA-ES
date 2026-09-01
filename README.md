# API-COTAÇÕES
API DE COTAÇÕES EM JSON PARA INFORMAÇÃO EM TEMPO REAL SOBRE BITCOIN E DOLAR


# 💰 API de Cotações (Dólar e Bitcoin)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

Uma API RESTful simples e rápida para consultar a cotação atual do **Dólar (USD/BRL)** e do **Bitcoin (BTC/BRL)** em tempo real. Os dados são obtidos da [Awesome API](https://docs.awesomeapi.com.br/), uma fonte pública e gratuita.

## ✨ Funcionalidades

- 📈 Busca individual ou simultânea das cotações.
- ⚡ Requisições assíncronas para máximo desempenho (busca Dólar e Bitcoin em paralelo).
- 📄 Documentação interativa automática via Swagger UI (`/docs`).
- 🌍 Configurado com CORS, pronto para ser consumido por aplicações front-end.
- 🚀 Deploy simplificado no Vercel.

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e de alto desempenho.
- **[HTTPX](https://www.python-httpx.org/)** - Cliente HTTP assíncrono para consumo das APIs externas.
- **[Pydantic](https://docs.pydantic.dev/)** - Validação e serialização de dados.
- **[Vercel](https://vercel.com/)** - Plataforma de hospedagem para serverless functions.

## 🚀 Como Rodar o Projeto Localmente

### Pré-requisitos

- Python 3.9 ou superior instalado.
- Pip (gerenciador de pacotes do Python).

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/api-cotacoes.git
   cd api-cotacoes
