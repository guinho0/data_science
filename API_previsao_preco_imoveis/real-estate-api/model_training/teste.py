import pandas as pd

# Substitua pelo caminho do seu arquivo
df = pd.read_csv('C:/Users/thiag/Desktop/API_previsao_preco_imoveis/real-estate-api/data/houses_to_rent.csv')

# Listar cidades únicas ordenadas
cidades = sorted(df['city'].unique())

# Exibir
print("Cidades encontradas na base:")
for cidade in cidades:
    print("-", cidade)
