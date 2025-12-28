import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def preprocess_gps(csv_path,sequence_length=10):
    df=pd.read_csv(csv_path)
    speeds=df[['speed']].values

    scaler=MinMaxScaler()
    scaled=scaler.fit_transform(speeds)

    X=[]
    y=[]
    for i in range(len(scaled)-sequence_length):
        X.append(scaled[i:i+sequence_length])
        y.append(scaled[i+sequence_length])

    return np.array(X),np.array(y),scaler
