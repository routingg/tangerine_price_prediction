import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from math import sqrt

# 데이터 로드
data = pd.read_csv('../data/price data.csv', sep=',')
xy = np.array(data, dtype=np.float32)

# 4개의 변인을 입력을 받습니다.
x_data = xy[:, 1:-1]

# 가격 값을 입력 받습니다.
y_data = xy[:, [-1]]

# 데이터를 훈련셋과 테스트셋으로 분리 (80% 훈련 데이터, 20% 테스트 데이터)
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

# Model 설정
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(1, input_shape=(4,))
])

# optimizer와 loss 설정
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.000005),
              loss='mse')

class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch % 500 == 0:
            print(f'{epoch} epochs, Training loss: {logs["loss"]}, Validation loss: {logs["val_loss"]}')

# Model 훈련
history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100000, callbacks=[CustomCallback()], verbose=0) 

# 모델 저장
model.save('my_model.h5') 
print('학습된 모델을 저장했습니다.')

# 모델 성능 평가
y_pred = model.predict(x_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = sqrt(mse)
r2 = r2_score(y_test, y_pred)

print('성능평가 결과입니다.')
print(f'MAE: {mae}')
print(f'MSE: {mse}')
print(f'RMSE: {rmse}')
print(f'R Squared: {r2}')

