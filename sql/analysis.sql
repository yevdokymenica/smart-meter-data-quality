-- 1. Основной запрос: расчет потребления по счетчикам и дням (только для валидных данных)
SELECT
    meter_id,
    CAST(timestamp AS DATE) AS consumption_date,
    ROUND(SUM(consumption_kwh)::numeric, 3) AS daily_consumption
FROM smart_meter_readings
WHERE quality_status = 'valid'
GROUP BY meter_id, CAST(timestamp AS DATE)
ORDER BY consumption_date, meter_id;

-- 2. Data Quality KPIs: сводный отчет по качеству данных
SELECT 
    COUNT(*) AS total_measurements,
    SUM(CASE WHEN quality_status = 'duplicate' THEN 1 ELSE 0 END) AS duplicate_measurements,
    SUM(CASE WHEN quality_status = 'invalid_negative' THEN 1 ELSE 0 END) AS invalid_values,
    SUM(CASE WHEN quality_status = 'anomaly' THEN 1 ELSE 0 END) AS anomalies,
    SUM(CASE WHEN quality_status = 'invalid_interval' THEN 1 ELSE 0 END) AS invalid_intervals,
    ROUND(
        (SUM(CASE WHEN quality_status = 'valid' THEN 1 ELSE 0 END)::numeric / COUNT(*)) * 100, 
        2
    ) AS data_quality_rate_percent
FROM smart_meter_readings;

-- 3. Проблемы по конкретным счетчикам (для таблицы в Power BI)
SELECT
    meter_id,
    SUM(CASE WHEN quality_status = 'duplicate' THEN 1 ELSE 0 END) AS duplicate_count,
    SUM(CASE WHEN quality_status = 'invalid_negative' THEN 1 ELSE 0 END) AS invalid_count,
    SUM(CASE WHEN quality_status = 'anomaly' THEN 1 ELSE 0 END) AS anomaly_count,
    ROUND(
        (SUM(CASE WHEN quality_status = 'valid' THEN 1 ELSE 0 END)::numeric / COUNT(*)) * 100, 
        2
    ) as quality_percentage
FROM smart_meter_readings
GROUP BY meter_id
ORDER BY quality_percentage ASC;