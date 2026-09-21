# Smart Meter Data Quality & Energy Consumption Analysis

## Objective
Entwicklung eines prototypischen Prozesses zur Verarbeitung und Qualitätssicherung von Smart-Meter-Messdaten.

## Project Pipeline
1. **Data Ingestion**: Generierung von synthetischen Smart-Meter-Rohdaten (30 Zähler, 7 Tage, 15-Minuten-Interwale).
2. **Data Validation**: Einlesen und Strukturierung der Zeitreihendaten mittels Python (Pandas/NumPy).
3. **Data Quality Checks**: Automatisierte Erkennung von:
   - Fehlenden Messwerten (Missing measurements)
   - Doppelten Zeitstempeln (Duplicate timestamps)
   - Negativen Verbrauchswerten (`consumption_kwh < 0`)
   - Unplausiblen Verbrauchsanomalien (> 10 kWh)
   - Ungültigen Intervallen
4. **Data Processing**: Markierung der Daten nach Qualitätsstatus und Speicherung als bereinigter Dataset.
5. **SQL Analysis**: Aggregation des täglichen Verbrauchs pro Zähler und Berechnung von Data-Quality-KPIs.
6. **Power BI Visualization**: Interaktives Dashboard zur Visualisierung von Verbrauchen und Qualitätskennzahlen.

## Business Relevance
Eine hohe Datenqualität ist eine wesentliche Voraussetzung für eine zuverlässige Verarbeitung von Mess- und Energiedaten. Der entwickelte Prototyp zeigt beispielhaft, wie fehlerhafte Messwerte identifiziert, validiert und für weitere Analysen aufbereitet werden können.

## Tech Stack
* **Python** (Pandas, NumPy)
* **SQL** / **PostgreSQL**
* **Power BI**