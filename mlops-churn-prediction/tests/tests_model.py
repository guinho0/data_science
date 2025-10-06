import pytest
import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Define o caminho do modelo salvo (deve existir após a etapa 5)
MODEL_PATH = os.path.join("models", "model.pkl")

# --- Testes de Qualidade e Existência do Modelo ---

def test_model_file_exists():
    """
    Verifica se o arquivo do modelo foi criado corretamente.
    """
    assert os.path.exists(MODEL_PATH), "O arquivo models/model.pkl não foi encontrado. Execute o treinamento primeiro."

def test_model_is_valid_type():
    """
    Verifica se o objeto carregado é um modelo treinado (Regressão Logística).
    """
    model = joblib.load(MODEL_PATH)
    assert isinstance(model, LogisticRegression), "O objeto carregado não é uma instância de Regressão Logística."

# --- Teste de Predição Simples ---

def test_model_prediction_output():
    """
    Verifica se o modelo retorna uma predição no formato correto (número).
    Os valores de entrada devem seguir o formato de treino:
    ['tenure', 'monthly_charges', 'gender', 'partner']
    gender e partner são 0 ou 1, conforme mapeamos.
    """
    model = joblib.load(MODEL_PATH)
    
    # Exemplo de um cliente com alta taxa de churn (ex: tenure baixo, charges altos)
    data_high_churn = pd.DataFrame([[1, 80.0, 0, 0]], 
                                    columns=['tenure', 'monthly_charges', 'gender', 'partner'])
    
    prediction = model.predict(data_high_churn)[0]
    
    # O modelo de classificação deve retornar 0 ou 1
    assert prediction in [0, 1], "A predição do modelo não é binária (0 ou 1)."

### Execução dos Testes

No terminal integrado do VS Code (Ubuntu), execute:

```bash
docker compose run api pytest tests/