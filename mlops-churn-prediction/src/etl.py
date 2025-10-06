import pandas as pd
from src.database import get_db_connection # Importa a conexão
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
    # A coluna TotalCharges é importada como string por conter espaços. 
    # Mapeamos espaços vazios para NaN e depois preenchemos com 0.0 (assumindo novos clientes).
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0.0) 
    
    # 2. Simplificação da coluna Churn (target) para Booleano
    # Mapeamos 'Yes' para True e 'No' para False. 
    # Renomeamos para 'churn' para corresponder ao esquema do DB.
    df['churn'] = df['Churn'].map({'Yes': True, 'No': False})
    
    # 3. Mapeamento das Features de Treinamento
    # Para o modelo de ML (Regressão Logística) ser mais simples, vamos usar as features
    # que mapeiam diretamente para números (0 ou 1):
    df['gender'] = df['gender'].map({'Female': 0, 'Male': 1})
    df['Partner'] = df['Partner'].map({'Yes': 1, 'No': 0})
    
    # 4. Seleção e Renomeação das Colunas Finais
    # Seleciona as colunas que correspondem ao esquema da tabela 'clientes' no PostgreSQL.
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
    Este é o método mais eficiente para carga em massa.
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
            conn.rollback() # Desfaz a transação em caso de erro
    finally:
        if conn:
            conn.close()

def run_etl():
    """Função principal do pipeline ETL."""
    # 1. Extração
    try:
        # Verifica se o arquivo está na pasta 'data'
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"ERRO: Arquivo '{DATA_PATH}' não encontrado. Baixe o 'churn.csv' e coloque na pasta 'data'.")
            
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