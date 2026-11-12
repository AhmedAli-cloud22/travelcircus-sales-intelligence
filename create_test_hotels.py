import pandas as pd

# Bestehende Hoteldaten laden
df = pd.read_csv("data/hotels.csv")

# Fünf Hotels als Testdaten verwenden
test_df = df.head(5).copy()

# Fiktive Hotelnamen vergeben
test_df["hotel_name"] = [
    "Alpenblick Wellness Resort",
    "Bergsee Spa Hotel",
    "Naturhotel Sonnenhof",
    "Panorama Wellness Lodge",
    "Seeblick Relax Resort"
]

# Als Excel-Datei speichern
test_df.to_excel("data/test_hotels.xlsx", index=False)

print("Excel-Datei erfolgreich erstellt!")
