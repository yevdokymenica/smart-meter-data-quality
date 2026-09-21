import pandas as pd
import random
from datetime import datetime, timedelta

def generate_smart_meter_data():
    random.seed(42)
    
    meters = [f"DE_{1000 + i}" for i in range(30)]
    start_time = datetime(2026, 6, 1, 0, 0, 0)
    end_time = start_time + timedelta(days=7)
    
    # Создаем временные интервалы (каждые 15 минут)
    timestamps = []
    current_ts = start_time
    while current_ts < end_time:
        timestamps.append(current_ts)
        current_ts += timedelta(minutes=15)
    
    data = []
    
    for meter in meters:
        for ts in timestamps:
            hour = ts.hour
            # Простая имитация суточного профиля с помощью пиков утром и вечером
            base_load = 0.2 + 0.3 * abs((hour - 12) / 12) # упрощенный аналог синусоиды
            noise = random.gauss(0, 0.05)
            consumption = max(0.01, round(base_load + noise, 3))
            
            data.append({
                "meter_id": meter,
                "timestamp": ts,
                "consumption_kwh": consumption,
                "status": "valid"
            })
            
    df = pd.DataFrame(data)
    
    # --- Внедрение проблем для Data Quality ---
    # 1. Пропуски (~1% строк)
    drop_indices = df.sample(frac=0.01, random_state=42).index
    df = df.drop(drop_indices)
    
    # 2. Дубликаты (20 строк)
    duplicates = df.sample(n=20, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 3. Отрицательные значения
    neg_indices = df.sample(n=15, random_state=123).index
    df.loc[neg_indices, "consumption_kwh"] = [-round(random.uniform(0.1, 1.0), 3) for _ in range(len(neg_indices))]
    
    # 4. Аномально высокий расход
    high_indices = df.sample(n=10, random_state=456).index
    df.loc[high_indices, "consumption_kwh"] = [round(random.uniform(15.0, 50.0), 3) for _ in range(len(high_indices))]
    
    # 5. Неправильные интервалы (смещение на 7 минут)
    shift_indices = df.sample(n=12, random_state=789).index
    df.loc[shift_indices, "timestamp"] = df.loc[shift_indices, "timestamp"] + timedelta(minutes=7)
    
    df = df.sort_values(by=["meter_id", "timestamp"]).reset_index(drop=True)
    
    df.to_csv("data/smart_meter_readings.csv", index=False)
    print(f"Dataset successfully created without NumPy! Total rows: {len(df)}")

if __name__ == "__main__":
    generate_smart_meter_data()