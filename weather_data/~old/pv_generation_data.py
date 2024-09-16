import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta 


# Funktion zur Berechnung des saisonalen Faktors basierend auf dem Tag des Jahres


def seasonal_factor(day_of_year):
    # Sinuskurve: Maximalwerte um den 172. Tag (21. Juni, Sommeranfang)
    return 0.5 * (1 + np.sin(2 * np.pi * (day_of_year - 172) / 365))

# Funktion zur Generierung der PV-Daten unter Berücksichtigung der Jahreszeiten
def generate_seasonal_pv_data(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    pv_data = []

    for date in date_range:
        day_of_year = date.timetuple().tm_yday

        # Bestimme den saisonalen Faktor basierend auf dem Tag des Jahres
        season_factor = seasonal_factor(day_of_year)

        # Tageszeitliche Variation (höchste Werte um die Mittagszeit)
        hour = date.hour
        daily_factor = max(0, np.sin((hour - 6) * np.pi / 12))  # Sonnenaufgang um 6 Uhr, Höchststand 12-14 Uhr

        # Grundwert für die Tagesleistung
        pv_value = season_factor * daily_factor

        # Bewölkte Tage einfügen
        month = date.month
        if 5 <= month <= 9:  # Mai bis September (sonnenreiche Monate)
            if random.random() < 0.05:  # 5% der Tage bewölkt
                pv_value *= random.uniform(0.2, 0.5)
        else:  # Oktober bis April (sonnenarme Monate)
            pv_value *= random.uniform(0.2, 0.4)  # Niedrigere Maximalwerte
            if random.random() < 0.3:  # 30% Wahrscheinlichkeit für Dunkelflauten
                pv_value *= random.uniform(0.0, 0.3)

        # Zufällige leichte Variationen hinzufügen
        pv_value = max(0, pv_value + random.uniform(-0.05, 0.05))

        pv_data.append([date, round(pv_value, 4)])

    return pd.DataFrame(pv_data, columns=['Datum', 'Normierte_Leistung'])

# Erstellen des neuen Datensatzes
start_date = '2023-01-01'
end_date = '2023-12-31'
pv_data_seasonal_df = generate_seasonal_pv_data(start_date, end_date)

# Speichern als neue CSV-Datei
csv_file_path_seasonal = 'pv_norddeutschland_2023_seasonal.csv'
pv_data_seasonal_df.to_csv(csv_file_path_seasonal, index=False)

csv_file_path_seasonal
