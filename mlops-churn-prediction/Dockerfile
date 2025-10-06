# Imagem base
FROM python:3.10-slim

# Variável de ambiente para evitar a criação de .pyc e buffer de saída
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . /app/