import pandas as pd
import numpy as np

def run_data_quality_pipeline():
    # 1. Ingestion
    df = pd.read_csv("data/smart_meter_readings.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    total_measurements = len(df)
    
    # Инициализируем колонку статуса качества
    df['quality_status'] = 'valid'
    
    # 2. Check: Duplicate timestamps per meter
    duplicates_mask = df.duplicated(subset=['meter_id', 'timestamp'], keep=False)
    df.loc[duplicates_mask, 'quality_status'] = 'duplicate'
    duplicate_count = duplicates_mask.sum()
    
    # 3. Check: Negative consumption
    neg_mask = (df['consumption_kwh'] < 0) & (df['quality_status'] == 'valid')
    df.loc[neg_mask, 'quality_status'] = 'invalid_negative'
    invalid_count = neg_mask.sum()
    
    # 4. Check: Anomalies (unusually high consumption > 10 kWh)
    anomaly_mask = (df['consumption_kwh'] > 10.0) & (df['quality_status'] == 'valid')
    df.loc[anomaly_mask, 'quality_status'] = 'anomaly'
    anomaly_count = anomaly_mask.sum()
    
    # 5. Check: Invalid intervals (minutes not in 0, 15, 30, 45)
    interval_mask = (~df['timestamp'].dt.minute.isin([0, 15, 30, 45])) & (df['quality_status'] == 'valid')
    df.loc[interval_mask, 'quality_status'] = 'invalid_interval'
    interval_error_count = interval_mask.sum()
    
    # Метрики качества данных
    total_issues = duplicate_count + invalid_count + anomaly_count + interval_error_count
    data_quality_rate = round((total_measurements - total_issues) / total_measurements * 100, 2)
    
    print("\n--- DATA QUALITY REPORT ---")
    print(f"Total Measurements: {total_measurements}")
    print(f"Duplicates: {duplicate_count}")
    print(f"Invalid Values (< 0): {invalid_count}")
    print(f"Anomalies (> 10 kWh): {anomaly_count}")
    print(f"Invalid Intervals: {interval_error_count}")
    print(f"Data Quality Rate: {data_quality_rate}%")
    
    # Сохраняем очищенные и размеченные данные
    df.to_csv("data/smart_meter_cleaned.csv", index=False)
    print("\nCleaned data saved to data/smart_meter_cleaned.csv")

if __name__ == "__main__":
    run_data_quality_pipeline()