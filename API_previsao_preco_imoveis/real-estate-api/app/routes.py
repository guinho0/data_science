import joblib
import pandas as pd
from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

# Carregar modelo e encoder
model = joblib.load('app/model.pkl')
encoder = joblib.load('app/encoder.pkl')

# Lista das cidades conhecidas pelo encoder
known_cities = encoder.categories_[0].tolist()

@main.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Validação de campos obrigatórios
        required_fields = ['city', 'rooms', 'bathrooms', 'parking', 'insurance']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório ausente: {field}'}), 400

        # Validação de tipos
        try:
            city = str(data['city'])
            rooms = int(data['rooms'])
            bathrooms = int(data['bathrooms'])
            parking = int(data['parking'])
            insurance = float(data['insurance'])
        except ValueError:
            return jsonify({'error': 'rooms, bathrooms, parking devem ser inteiros e insurance deve ser número decimal'}), 400

        # Validação da cidade
        if city not in known_cities:
            return jsonify({
                'error': 'Cidade não encontrada. Use uma das cidades: ' + ', '.join(known_cities)
            }), 400

        # Codificar a cidade
        city_df = pd.DataFrame([[city]], columns=['city'])
        city_encoded = encoder.transform(city_df)
        city_encoded_df = pd.DataFrame(city_encoded, columns=encoder.get_feature_names_out(['city']))

        # Criar DataFrame com todas as features
        input_df = pd.concat([
            city_encoded_df,
            pd.DataFrame([[rooms, bathrooms, parking, insurance]], columns=['rooms', 'bathrooms', 'parking', 'insurance'])
        ], axis=1)

        # Fazer a previsão
        prediction = model.predict(input_df)[0]

        return jsonify({'predicted_rent': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'online'})
