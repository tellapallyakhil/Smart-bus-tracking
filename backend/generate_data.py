import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
BUSES = ['BUS_01', 'BUS_02', 'BUS_03']
ROUTES = {
    'BUS_01': ['Secunderabad', 'Paradise', 'Tank Bund', 'Secretariat', 'Charminar'],
    'BUS_02': ['Hitech City', 'Jubilee Hills', 'Punjagutta', 'Koti', 'LB Nagar'],
    'BUS_03': ['Mehdipatnam', 'Lakdikapul', 'Abids', 'Afzal Gunj', 'Falaknuma']
}

# Base Distances (km) between stops (approximate)
DISTANCES = [0, 2.5, 5.0, 8.0, 12.0] 
AVG_SPEED_KMH = 25

def generate_trip_data(num_days=7):
    data = []
    
    start_date = datetime.now() - timedelta(days=num_days)
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        for bus_id in BUSES:
            route_stops = ROUTES[bus_id]
            
            # Simulate 10 trips per day per bus
            for trip_num in range(10):
                # Random start time between 6 AM and 8 PM
                start_hour = random.randint(6, 20)
                trip_start_time = current_date.replace(hour=start_hour, minute=random.randint(0, 59))
                
                # Base Traffic Factor (1.0 = normal, 1.5 = heavy)
                # Heavy traffic during peaks: 8-10 AM, 5-7 PM
                is_peak = (8 <= start_hour <= 10) or (17 <= start_hour <= 19)
                traffic_factor = random.uniform(1.3, 1.8) if is_peak else random.uniform(0.9, 1.2)
                
                for i in range(len(route_stops)):
                    stop_name = route_stops[i]
                    
                    if i == 0:
                        arrival_time = trip_start_time
                        travel_time_min = 0
                    else:
                        # Time = Distance / Speed
                        segment_dist = DISTANCES[i] - DISTANCES[i-1]
                        base_time_hours = segment_dist / AVG_SPEED_KMH
                        
                        # Apply traffic variability
                        actual_time_hours = base_time_hours * traffic_factor
                        travel_time_min = int(actual_time_hours * 60)
                        
                        arrival_time = arrival_time + timedelta(minutes=travel_time_min)

                    # --- Prediction Logic ---
                    # Estimated Time of Arrival (ETA) calculation
                    # Smart prediction tries to guess traffic but isn't perfect
                    predicted_traffic_factor = traffic_factor * random.uniform(0.9, 1.1) 
                    
                    # Target Arrival (Scheduled) - assume schedule is based on pure 25km/h
                    scheduled_time_from_start = (DISTANCES[i] / AVG_SPEED_KMH) * 60
                    scheduled_arrival = trip_start_time + timedelta(minutes=scheduled_time_from_start)
                    
                    # Delay Calculation (Actual - Scheduled)
                    delay_minutes = (arrival_time - scheduled_arrival).total_seconds() / 60
                    
                    # Rating Logic (1-5 Stars)
                    # < 0 min delay (early) -> 5
                    # 0-5 min delay -> 4
                    # 5-10 min delay -> 3
                    # 10-20 min delay -> 2
                    # > 20 min delay -> 1
                    if delay_minutes <= 0: rating = 5
                    elif delay_minutes <= 5: rating = 4
                    elif delay_minutes <= 10: rating = 3
                    elif delay_minutes <= 20: rating = 2
                    else: rating = 1
                    
                    record = {
                        "Trip_ID": f"TRIP_{day}_{bus_id}_{trip_num}",
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "Bus_ID": bus_id,
                        "Stop_Name": stop_name,
                        "Sequence_No": i + 1,
                        "Scheduled_Arrival": scheduled_arrival.strftime("%H:%M:%S"),
                        "Actual_Arrival": arrival_time.strftime("%H:%M:%S"),
                        "Delay_Minutes": round(delay_minutes, 2),
                        "Traffic_Condition": "Heavy" if is_peak else "Normal",
                        "Prediction_Accuracy": "High" if abs(delay_minutes) < 5 else "Low",
                        "Rating": rating
                    }
                    data.append(record)
                    
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating synthetic bus data...")
    df = generate_trip_data(num_days=30)
    
    # Analyze
    print("\n--- Data Summary ---")
    print(df.groupby('Bus_ID')['Rating'].mean())
    
    filename = "bus_data_predictions.csv"
    df.to_csv(filename, index=False)
    print(f"\nSuccessfully generated {len(df)} records.")
    print(f"Saved to: {filename}")
