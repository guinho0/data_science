# 🏠 API de Previsão de Aluguel

Este projeto é uma API REST desenvolvida com **Flask** que utiliza um modelo de regressão treinado para prever o valor do aluguel de imóveis no Brasil, com base em dados como cidade, número de quartos, banheiros, vagas de garagem e valor do seguro (`insurance`).

---

## 📦 Estrutura do Projeto

```
project/
│
├── app/
│   ├── __init__.py            # Inicialização da aplicação Flask
│   ├── routes.py              # Rotas da API (inclui endpoint /predict)
│   ├── model.pkl              # Modelo de regressão treinado
│   ├── encoder.pkl            # OneHotEncoder salvo com cidades
│
├── data/
│   └── aluguel.csv            # Dataset original (exemplo)
│
├── static/
│   └── swagger.yaml           # Documentação da API em formato OpenAPI
│
├── train_model.py             # Script para treinar o modelo
├── run.py                     # Arquivo principal para rodar o servidor Flask
└── README.md                  # Este arquivo
```

---

## 🚀 Como Executar o Projeto

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

Exemplo de `requirements.txt`:
```txt
Flask
pandas
scikit-learn
joblib
flask-swagger-ui
```

---

### 2. Treine o modelo (se ainda não tiver os arquivos `model.pkl` e `encoder.pkl`)

```bash
python train_model.py
```

Esse script irá:

- Ler os dados do CSV
- Codificar a coluna `city`
- Treinar um modelo de regressão
- Salvar o modelo (`model.pkl`) e o encoder (`encoder.pkl`)

---

### 3. Execute a API Flask

```bash
python run.py
```

A API estará disponível em:  
👉 `http://127.0.0.1:5000`

---

## 🧪 Endpoints

### `POST /predict`

Realiza a previsão do aluguel.

#### Corpo da Requisição (JSON):

```json
{
  "city": "Campinas",
  "rooms": 2,
  "bathrooms": 1,
  "parking": 1,
  "insurance": 30.5
}
```

#### Resposta esperada:

```json
{
  "predicted_rent": 2350.75
}
```

---

### `GET /cities`

Lista as cidades disponíveis no modelo.

#### Exemplo de resposta:

```json
{
  "cities": ["São Paulo", "Campinas", "Salvador", "Recife"]
}
```

---

### `GET /health`

Verifica se a API está online.

#### Resposta:

```json
{
  "status": "online"
}
```

---

### `GET /docs`

Acessa a documentação da API com Swagger UI.

---

## 📊 Dataset Utilizado

O projeto usa um dataset de aluguel de imóveis contendo colunas como:

- `city` — cidade do imóvel
- `rooms` — número de quartos
- `bathrooms` — número de banheiros
- `parking` — número de vagas
- `insurance` — valor do seguro
- `rent_amount` — valor do aluguel (variável alvo)

---

## 🤖 Modelo

- Tipo: `LinearRegression` (scikit-learn)
- Features utilizadas:
  - Cidade (OneHotEncoded)
  - Número de quartos
  - Número de banheiros
  - Número de vagas
  - Seguro (`insurance`)

---

## 📌 To Do

- [x] Treinar modelo com coluna `insurance`
- [x] Criar endpoint `/predict`
- [x] Adicionar validações robustas
- [x] Criar endpoint `/cities`
- [ ] Adicionar testes automatizados
- [ ] Dockerizar aplicação

---

## 👨‍💻 Autor

**Thiago**  
Estudante de Sistemas de Informação no Ifes - Campus Serra  
Estagiário na área de Dados, com interesse em Ciência de Dados e Desenvolvimento de APIs.

---

## 📄 Licença

Este projeto é livre para fins educacionais. Consulte a licença do dataset original se aplicável.