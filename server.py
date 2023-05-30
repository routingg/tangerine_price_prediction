from flask import Flask, render_template, request, jsonify
import numpy as np
import pymysql
from config import DB_CONFIG
import tensorflow as tf

app = Flask(__name__, static_folder='static')

# 저장된 모델을 불러옵니다.
model = tf.keras.models.load_model('model/my_model.h5')

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 파라미터를 전달 받습니다.
        data = request.get_json(force=True)

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        avg_temp = float(data.get('avg_temp', 0))
        min_temp = float(data.get('min_temp', 0))
        max_temp = float(data.get('max_temp', 0))
        rain_fall = float(data.get('rain_fall', 0))

        if any(v is None for v in [avg_temp, min_temp, max_temp, rain_fall]):
            return jsonify({'error': 'No data provided or data is not in JSON format'}), 400

        # 입력된 파라미터를 배열 형태로 준비합니다.
        input_data = np.array([[avg_temp, min_temp, max_temp, rain_fall]], dtype=np.float32)

        # 입력 값을 토대로 예측 값을 찾아냅니다.
        predicted = model.predict(input_data)

        # 결과 가격을 저장합니다.
        price = float(predicted[0][0])
        return jsonify(price=price)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-price-data')
def getPriceData():
    connection = pymysql.connect(**DB_CONFIG)

    cursor = connection.cursor()
    cursor.execute('SELECT DATE_FORMAT(weather_data.date, "%Y%m") AS month, AVG(citrus_price_data.avgPrice) AS avg_monthly_price '
                   'FROM citrus_price_data '
                   'JOIN weather_data ON citrus_price_data.weather_id = weather_data.weather_id '
                   'GROUP BY month '
                   'ORDER BY month')
    results = cursor.fetchall()

    data = {
        'months': [row[0] for row in results],
        'avgPrices': [row[1] for row in results]
    }

    connection.close()
    return jsonify(months=data['months'], avgPrices=data['avgPrices'])

@app.route('/get-weather-data')
def getWeatherData():
    connection = pymysql.connect(**DB_CONFIG)

    cursor = connection.cursor()
    cursor.execute('SELECT DATE_FORMAT(weather_data.date, "%Y%m") AS month, AVG(weather_data.avgTemp) AS avg_monthly_temp, AVG(weather_data.rainFall) AS avg_monthly_rainfall '
                   'FROM weather_data '
                   'GROUP BY month '
                   'ORDER BY month DESC LIMIT 12')
    results = cursor.fetchall()

    data = {
        'months': [row[0] for row in results],
        'avgTemps': [row[1] for row in results],
        'avgRainfalls': [row[2] for row in results]
    }

    connection.close()
    return jsonify(months=data['months'], avgTemps=data['avgTemps'], avgRainfalls=data['avgRainfalls'])


if __name__ == '__main__':
    app.run(debug=True)
