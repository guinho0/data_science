from fastapi import FastAPI, HTTPException
from src.schemas import CustomerFeatures
import joblib
import pandas as pd
import os
import time
from src.database import get_db_connection # Importa a função de conexão

# Define o caminho para o modelo serializado
MODEL_PATH = os.path.join("models", "model.pkl")

# Inicializa o FastAPI
app = FastAPI(title="MLOps Churn Predictor")

# Variável global para armazenar o modelo
model = None

def load_model():
    """Tenta carregar o modelo treinado do disco."""
    global model
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")
        model = joblib.load(MODEL_PATH)
        print("Modelo carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        # Em produção, um erro aqui impediria a API de iniciar
        raise RuntimeError("Falha ao inicializar o modelo de ML.")

@app.on_event("startup")
async def startup_event():
    """Executado quando a aplicação inicia. Carrega o modelo."""
    load_model()

def log_prediction_to_db(features: CustomerFeatures, prediction: int):
    """Função bônus: Salva a predição e os inputs no PostgreSQL."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Insere a predição e os inputs (simplificado)
            cur.execute("""
                INSERT INTO prediction_logs (
                    tenure, monthly_charges, gender, partner, prediction, created_at
                ) VALUES (%s, %s, %s, %s, %s, NOW());
            """, (
                features.tenure,
                features.monthly_charges,
                features.gender,
                features.partner,
                bool(prediction) # Salva como booleano no DB
            ))
            conn.commit()
    except Exception as e:
        # Se falhar, registra no console, mas não impede a predição de ser retornada
        print(f"Aviso: Falha ao logar a predição no DB: {e}")
    finally:
        if conn:
            conn.close()

# Rota de Saúde/Verificação
@app.get("/health")
def check_health():
    """Verifica se a API está no ar e se o modelo foi carregado."""
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo de ML não carregado.")
    return {"status": "ok", "model_loaded": True, "timestamp": time.time()}

# Rota Principal de Predição
@app.post("/predict")
def predict_churn(features: CustomerFeatures):
    """Recebe dados de um cliente e retorna a probabilidade de Churn."""
    
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo de ML indisponível.")

    try:
        # Converte os dados de entrada Pydantic para um DataFrame Pandas
        input_df = pd.DataFrame([features.dict()])
        
        # Faz a predição
        prediction = model.predict(input_df)[0]
        # Pega a probabilidade do churn (classe 1)
        probability_churn = model.predict_proba(input_df)[0][1]

        # Loga a predição no banco de dados (BÔNUS)
        log_prediction_to_db(features, int(prediction))
        
        return {
            "prediction": int(prediction), # 1 (Churn) ou 0 (No Churn)
            "probability_churn": round(probability_churn, 4),
            "input_features": features.dict()
        }
    except Exception as e:
        print(f"Erro na predição: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a predição.")