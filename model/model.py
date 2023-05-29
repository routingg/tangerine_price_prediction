import tensorflow as tf
import numpy as np
import pandas as pd

data = pd.read_csv('../data/price data.csv', sep=',')

xy = np.array(data, dtype=np.float32)

# 4개의 변인을 입력을 받습니다.
x_data = xy[:, 1:-1]

# 가격 값을 입력 받습니다.
y_data = xy[:, [-1]]

# Model 설정
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(1, input_shape=(4,))
])

# optimizer와 loss 설정
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.000005),
              loss='mse')

# Model 훈련
history = model.fit(x_data, y_data, epochs=100000) 

# 모델 저장
model.save('my_model.h5') 
print('학습된 모델을 저장했습니다.')
