from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense

def build_lstm():
    model=Sequential()
    model.add(LSTM(64,input_shape=(10,1)))
    model.add(Dense(1))
    model.compile(optimizer="adam",loss="mse")
    return model
