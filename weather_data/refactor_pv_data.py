import pandas as pd

# Zeitreihe aus einer CSV-Datei laden
df = pd.read_csv('weather_data/pv_data_adjusted_3.csv', parse_dates=['Timestamp'])

# Index auf den Timestamp setzen, um einfacheres Arbeiten zu ermöglichen
df.set_index('Timestamp', inplace=True)

# Alle Indizes von 'PV Power', die den Wert 1 haben, finden
indices_with_ones = df[df['PV Power'] == 1].index

# Jeden zweiten Eintrag, der 1 ist, auf 0.5 setzen
for i in range(1, len(indices_with_ones), 2):  # Beginne bei 1, um jeden zweiten zu erreichen
    df.loc[indices_with_ones[i], 'PV Power'] = 0.5

# Die veränderte Zeitreihe ausgeben oder in eine neue Datei speichern
print("Die veränderte Zeitreihe:")
print(df.head(10))  # Beispielausgabe der ersten 10 Zeilen
df.to_csv('weather_data\pv_data_adjusted_2_updated.csv')
