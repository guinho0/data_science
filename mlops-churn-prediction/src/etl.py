import pandas as pd
from src.database import get_db_connection
import io
import os
import numpy as np

# Constantes do projeto
DATA_PATH = os.path.join("data", "churn.csv")
TABLE_NAME = "clientes"

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pré-processamento de dados no dataset de churn.
    Inclui limpeza, tratamento de valores e mapeamento para o modelo.
    """
    print("Iniciando pré-processamento...")
    
    # 1. Tratamento da coluna TotalCharges (Contém espaços vazios que são NaN)
    # Coerce errors: transforma ' ' em NaN.
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # 2. Simplificação da coluna Churn (target) para Booleano
    df['churn'] = df['Churn'].map({'Yes': True, 'No': False})
    
    # 3. Mapeamento das Features de Treinamento para Numérico (0 ou 1)
    # O modelo de ML precisa de números, não strings.
    df['gender'] = df['gender'].map({'Female': 0, 'Male': 1})
    df['Partner'] = df['Partner'].map({'Yes': 1, 'No': 0})
    
    # 4. Imputação de zeros para quaisquer NaN remanescentes.
    # Esta linha corrige o problema 'Input X contains NaN'.
    # Usamos 0.0 para imputar NaNs em colunas numéricas (TotalCharges, tenure, MonthlyCharges, etc.).
    df = df.fillna(0.0) 
    
    # 5. Seleção e Renomeação das Colunas Finais
    # Selecionamos apenas as colunas que definimos no nosso esquema SQL.
    final_columns = {
        'customerID': 'customer_id',
        'gender': 'gender',
        'SeniorCitizen': 'senior_citizen',
        'Partner': 'partner',
        'tenure': 'tenure',
        'MonthlyCharges': 'monthly_charges',
        'churn': 'churn'
    }
    
    df_clean = df.rename(columns=final_columns)
    
    # Filtra apenas as colunas necessárias e na ordem correta
    df_clean = df_clean.filter(items=final_columns.values())

    print("Pré-processamento concluído.")
    return df_clean

def load_data_to_sql(df: pd.DataFrame):
    """
    Carrega o DataFrame limpo no PostgreSQL usando o método COPY.
    """
    conn = None
    try:
        conn = get_db_connection()
        
        # Cria um buffer de memória para exportar o DataFrame como CSV temporário
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)
        
        with conn.cursor() as cur:
            # Comando COPY do PostgreSQL para inserir todos os dados de uma vez
            cur.copy_from(buffer, TABLE_NAME, sep=",", columns=df.columns)
            conn.commit()
            print(f"Sucesso: {len(df)} linhas carregadas na tabela '{TABLE_NAME}'.")

    except Exception as e:
        print(f"Erro durante a carga de dados para o SQL: {e}")
        if conn:
            conn.rollback() 
    finally:
        if conn:
            conn.close()

def run_etl():
    """Função principal do pipeline ETL."""
    # 1. Extração
    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"ERRO: Arquivo '{DATA_PATH}' não encontrado.")
            
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"Falha na Extração: {e}")
        return

    # 2. Transformação
    df_clean = preprocess_data(df)
    
    # 3. Carga
    load_data_to_sql(df_clean)

if __name__ == '__main__':
    run_etl()
