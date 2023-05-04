import tensorflow.compat.v1 as tf
from flask import Flask, render_template, request, jsonify
import numpy as np
import pymysql

tf.disable_v2_behavior()

app = Flask(__name__, static_folder='static')

# 플레이스 홀더를 설정합니다.
X = tf.placeholder(tf.float32, shape=[None, 4])
Y = tf.placeholder(tf.float32, shape=[None, 1])
W = tf.Variable(tf.random_normal([4, 1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="bias")

# 가설을 설정합니다.
hypothesis = tf.matmul(X, W) + b

# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.train.Saver()
model = tf.global_variables_initializer()

# 세션 객체를 생성합니다.
sess = tf.Session()
sess.run(model)

# 저장된 모델을 세션에 적용합니다.
save_path = "./model/saved.cpkt"
saver.restore(sess, save_path)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 파라미터를 전달 받습니다.
    avg_temp = float(request.form['avg_temp'])
    min_temp = float(request.form['min_temp'])
    max_temp = float(request.form['max_temp'])
    rain_fall = float(request.form['rain_fall'])
    # 감귤 가격 변수를 선언합니다.
    price = 0
    # 입력된 파라미터를 배열 형태로 준비합니다.
    data = ((avg_temp, min_temp, max_temp, rain_fall), (0, 0, 0, 0))
    arr = np.array(data, dtype=np.float32)
    # 입력 값을 토대로 예측 값을 찾아냅니다.
    x_data = arr[0:4]
    dict = sess.run(hypothesis, feed_dict={X: x_data})
    # 결과 감귤 가격을 저장합니다.
    price = dict[0]
    return render_template('index.html', price=price)

@app.route('/data')
def data():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='tangerine_market_info')

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

if __name__ == '__main__':
    app.run(debug=True)

