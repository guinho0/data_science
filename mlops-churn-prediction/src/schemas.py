from pydantic import BaseModel

# Esquema para os dados de entrada que a API irá receber
class CustomerFeatures(BaseModel):
    """
    Define os atributos de um cliente para predição.
    Os nomes e tipos de dados devem corresponder ao modelo treinado.
    """
    tenure: int # Tempo de cliente (meses)
    monthly_charges: float # Custo mensal
    gender: int # 0 para Female, 1 para Male
    partner: int # 0 para No, 1 para Yes