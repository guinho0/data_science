import os
import psycopg2
from psycopg2 import sql

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL.
    As credenciais são lidas das variáveis de ambiente do Docker Compose.
    """
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "churn_db"),
            user=os.environ.get("DB_USER", "user"),
            password=os.environ.get("DB_PASS", "password")
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise e

def create_table_if_not_exists(conn):
    """
    Cria a tabela 'clientes' se ela ainda não existir.
    (O esquema da tabela é um exemplo baseado em um dataset de Churn.)
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                customer_id VARCHAR(255) UNIQUE,
                gender VARCHAR(50),
                senior_citizen INTEGER,
                partner VARCHAR(50),
                tenure INTEGER,
                monthly_charges NUMERIC,
                churn BOOLEAN
            );
        """)
        conn.commit()
    print("Tabela 'clientes' verificada/criada com sucesso.")

if __name__ == '__main__':
    # Teste de conexão e criação de tabela
    try:
        conn = get_db_connection()
        create_table_if_not_exists(conn)
        conn.close()
        print("Conexão com PostgreSQL bem-sucedida e encerrada.")
    except Exception as e:
        print(f"Teste de conexão falhou: {e}")