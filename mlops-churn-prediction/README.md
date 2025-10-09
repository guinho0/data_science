 MLOps Pipeline: Previsão de Rotatividade de Clientes (Customer Churn)
Este projeto demonstra uma arquitetura de Machine Learning (MLOps) de ponta a ponta para prever a rotatividade de clientes (Churn) utilizando um conjunto de dados real da IBM.

O pipeline abrange desde a ingestão e limpeza de dados até o treinamento do modelo e o deploy em uma API, tudo orquestrado via Docker.

 Tecnologias e Habilidades Praticadas
Área

Tecnologia

Habilidade Principal

Linguagem & ML

Python

Pandas, scikit-learn, Programação Orientada a Objetos (POO).

Infraestrutura

Docker, Docker Compose

Containerização, Orquestração de serviços (db e api), Volumes.

Dados

PostgreSQL (SQL)

Consulta, Carga em massa (COPY) e Persistência de dados limpos e logs.

Deploy

FastAPI

Criação de API REST para servir o modelo em produção.

Qualidade

Pytest

Testes de unidade para garantir a funcionalidade do modelo.

Controle

Git/GitHub

Versionamento de todo o código e infraestrutura.

 Como Rodar o Projeto (Guia Passo a Passo)
Para rodar o projeto, você precisa ter o Docker Desktop (ou Docker Engine) e o Git instalados e funcionando no seu terminal Linux (recomendado WSL/Ubuntu).

1. Clonar e Navegar
Clone o repositório e entre na pasta do projeto:

git clone SEU_LINK_DO_REPOSITORIO.git
cd mlops-churn-prediction

2. Configuração do Ambiente e Inicialização do DB
Este comando inicializa os containers, mas apenas sobe o banco de dados (db) para que possamos carregar os dados.

# Sobe o container do PostgreSQL em background
docker compose up -d db

3. Carga de Dados (ETL)
O arquivo churn.csv deve estar na pasta data/.

Etapa

Script

Comando

Criar Tabelas

src/database.py

Cria as tabelas clientes e prediction_logs no PostgreSQL.

Carga ETL

src/etl.py

Lê o CSV, faz a limpeza de NaN (Pandas), mapeia colunas e carrega os dados limpos no PostgreSQL (SQL).

Execute os comandos:

# 3.1. Cria as tabelas iniciais
docker compose run api python src/database.py

# 3.2. Executa o pipeline ETL e carrega 7043 linhas no PostgreSQL
docker compose run --build api python src/etl.py

4. Treinamento e Testes de Qualidade
Esta fase treina o modelo de Machine Learning e valida sua funcionalidade.

Etapa

Script

Comando

Treinamento ML

src/train_model.py

Consulta o DB, treina a Regressão Logística e salva o model.pkl localmente.

Testes de Unidade

tests/test_model.py

Executa o Pytest para validar a estrutura do modelo e o formato da predição.

Execute os comandos:

# 4.1. Treina o modelo e salva em ./models/model.pkl
docker compose run api python src/train_model.py

# 4.2. Roda os testes (deve retornar 3 passed)
docker compose run api pytest tests/

5. Deploy da API e Teste Final
A API agora expõe seu modelo via HTTP, permitindo que qualquer aplicação solicite uma previsão.

Etapa

Script

Comando

Deploy Final

src/main.py

Inicia os serviços db e api (FastAPI) em background.

Teste de Predição

curl

Envia dados simulados para a porta 8000 da API.

Execute os comandos:

# 5.1. Sobe todos os serviços (PostgreSQL e FastAPI)
docker compose up -d

# 5.2. Testa a API com um cliente que tem alta probabilidade de Churn
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
    "tenure": 5, 
    "monthly_charges": 95.5, 
    "gender": 1, 
    "partner": 0
}'

A resposta será um JSON com a prediction (0 ou 1) e a probability_churn.

📈 Próximos Passos e Aprimoramentos
O modelo atual de Regressão Logística é um ponto de partida para validar a arquitetura. Notamos que a Acurácia do Modelo no Teste está em torno de 79.3%, o que é aceitável, mas pode ser significativamente melhorado.

Este projeto pode ser expandido de várias formas para demonstrar proficiência avançada em Ciência de Dados e MLOps:

Melhoria da Modelagem e Acurácia:

Engenharia de Features: Criar novas colunas (ex: agrupar tenure em faixas de tempo).

Modelos Mais Complexos: Substituir a Regressão Logística por modelos de ensemble, como Random Forest ou XGBoost, que geralmente apresentam melhor acurácia para problemas de classificação.

Pré-processamento na API:

Atualmente, a API espera gender e partner como números (0 ou 1). O ideal é que a API aceite strings ("Male", "Yes") e faça a conversão internamente, usando um pipeline (ex: ColumnTransformer do scikit-learn) que seria salvo junto com o modelo.

Monitoramento e Orchestration (MLOps Real):

Orquestração de Pipeline: Integrar ferramentas como Apache Airflow ou Prefect para agendar e automatizar as etapas de ETL e Treinamento (que atualmente são executadas manualmente via docker compose run).

Monitoramento de Drift: Adicionar um dashboard (ex: com Streamlit) para monitorar o desempenho do modelo em produção e alertar sobre a degradação da acurácia ao longo do tempo.

