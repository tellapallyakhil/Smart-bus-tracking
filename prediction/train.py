from preprocess import preprocess_gps
from lstm_model import build_lstm

X,y,_=preprocess_gps("data/gps/bus_gps.csv")

model=build_lstm()
model.fit(X,y,epochs=20,batch_size=16)

model.save("models/lstm_eta.h5")
print("ETA Model Trained & Saved")
