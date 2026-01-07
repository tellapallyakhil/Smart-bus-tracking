import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load Data
try:
    df = pd.read_csv('bus_data_predictions.csv')
    print("Data Loaded Successfully.")
except FileNotFoundError:
    print("Error: bus_data_predictions.csv not found. Run generate_data.py first.")
    exit()

# Preprocessing
# We want to predict 'Delay_Minutes' based on: 'Bus_ID', 'Stop_Name', 'Hour_Of_Day'

# 1. Convert Timestamps to meaningful numeric features
df['Hour'] = pd.to_datetime(df['Scheduled_Arrival']).dt.hour
df['Minute'] = pd.to_datetime(df['Scheduled_Arrival']).dt.minute

# 2. Encode Categorical Data
le_bus = LabelEncoder()
df['Bus_ID_Code'] = le_bus.fit_transform(df['Bus_ID'])

le_stop = LabelEncoder()
df['Stop_Code'] = le_stop.fit_transform(df['Stop_Name'])

# Features (X) and Target (y)
X = df[['Bus_ID_Code', 'Stop_Code', 'Hour', 'Minute']]
y = df['Delay_Minutes']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model (Random Forest is robust allows for non-linear relationships like traffic peaks)
print("Training Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Model R2 Score: {score:.4f}")

# Save Artifacts
joblib.dump(model, 'backend/eta_model.pkl')
joblib.dump(le_bus, 'backend/le_bus.pkl')
joblib.dump(le_stop, 'backend/le_stop.pkl')

print("Model saved to backend/eta_model.pkl")
