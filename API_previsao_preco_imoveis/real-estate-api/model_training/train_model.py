import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 1. Carregar os dados
df = pd.read_csv('data/houses_to_rent.csv')  # Substitua com o nome correto do seu arquivo

# 2. Selecionar colunas de interesse
df = df[['city', 'rooms', 'bathroom', 'parking spaces', 'fire insurance (R$)', 'rent amount (R$)']]
df = df.dropna()

# 3. Separar variáveis preditoras e variável alvo
X = df[['city', 'rooms', 'bathroom', 'parking spaces', 'fire insurance (R$)']] # X = variáveis de entrada
y = df['rent amount (R$)']                                                     # y = alvo

# 4. Criar pipeline de pré-processamento + regressão
categorical_features = ['city'] #coluna categórica que precisa ser convertida em numero.
categorical_transformer = OneHotEncoder(handle_unknown='ignore') #handle_unknown evita erro caso uma cidade desconhecida seja adicionada


#columnTransformer aplica OneHotEncoder em "city"
preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)],
    remainder='passthrough'  # mantém as as colunas restantes como estão
)

#Cria um pipeline: um objeto que automatiza o fluxo:

#Pré-processa os dados.

#Aplica regressão linear.
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# 5. Dividir dados e treinar o modelo 80% para treino e 20% para teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train) #treina o modelo

# 6. Salvar o modelo treinado
joblib.dump(model, 'model.pkl') #salva o modelo treinado

print("✅ Modelo treinado e salvo com sucesso!")
