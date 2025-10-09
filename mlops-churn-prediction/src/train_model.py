import pandas as pd
from src.database import get_db_connection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = os.path.join("models", "model.pkl")

def train_and_save_model():
    """
    1. Carrega os dados limpos do PostgreSQL.
    2. Treina um modelo (Regressão Logística).
    3. Salva o modelo serializado no disco.
    """
    conn = None
    try:
        conn = get_db_connection()
        
        # 1. Consulta SQL para carregar os dados
        df = pd.read_sql(f"SELECT * FROM clientes", conn)
        print(f"Dados carregados do PostgreSQL: {len(df)} linhas.")
        
        # O mapeamento de strings não é mais necessário aqui, pois o ETL já fez isso.
        
        # Preparação X (features) e y (target)
        # Selecionamos as 4 features que serão usadas para a predição na API
        X = df[['tenure', 'monthly_charges', 'gender', 'partner']] 
        y = df['churn']
        
        # CORREÇÃO CRUCIAL: Garante que não haja NaNs que o ETL possa ter deixado
        # (Embora o ETL devesse ter limpado, esta é uma linha de robustez de ML)
        X = X.fillna(0.0) 
        
        # Divisão de dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 2. Treinamento do Modelo
        model = LogisticRegression(solver='liblinear', random_state=42)
        model.fit(X_train, y_train)
        
        # Avaliação
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Acurácia do Modelo no Teste: {accuracy:.4f}")
        
        # 3. Salva o Modelo (Serialização)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        print(f"Modelo salvo em: {MODEL_PATH}")

    except Exception as e:
        print(f"Erro durante o treinamento do modelo: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    train_and_save_model()
