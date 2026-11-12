import pandas as pd
from pathlib import Path

# 1. CSV-Datei einlesen
df = pd.read_csv("data/hotels.csv")

# 2. Mindestanforderungen überprüfen
df["qualified"] = (
    (df["google_rating"] >= 4.0)
    & (df["rooms"] >= 30)
    & (df["pool"] == True)
    & (df["wellness_score"] >= 3)
)

# 3. Einzelne Kriterien auf 0 bis 100 skalieren
df["wellness_points"] = df["wellness_score"] * 20
df["image_points"] = df["image_score"] * 20
df["reputation_points"] = df["google_rating"] * 20
df["demand_points"] = df["demand_score"] * 20

# Zimmerkapazität: 30 Zimmer = 60 Punkte,
# 150 oder mehr Zimmer = 100 Punkte
df["capacity_points"] = (
    60 + (df["rooms"] - 30) / 120 * 40
).clip(lower=0, upper=100)

# 4. Gewichteten Gesamtscore berechnen
df["lead_score"] = (
    df["wellness_points"] * 0.30
    + df["image_points"] * 0.25
    + df["reputation_points"] * 0.20
    + df["demand_points"] * 0.15
    + df["capacity_points"] * 0.10
).round(1)

# 5. Prioritätskategorie bestimmen
def assign_priority(row):
    if not row["qualified"]:
        return "Nicht qualifiziert"
    elif row["lead_score"] >= 80:
        return "A"
    elif row["lead_score"] >= 60:
        return "B"
    else:
        return "C"

df["priority"] = df.apply(assign_priority, axis=1)

# 6. Nach Qualifikation und Score sortieren
df = df.sort_values(
    by=["qualified", "lead_score"],
    ascending=[False, False]
)

# 7. Ergebnisse speichern
Path("data").mkdir(exist_ok=True)
df.to_csv("data/scored_hotels.csv", index=False)

# 8. Ergebnisse im Terminal anzeigen
print("\n--- LEAD SCORING ERGEBNIS ---")
print("Hotels insgesamt:", len(df))
print("Qualifiziert:", df["qualified"].sum())
print("Nicht qualifiziert:", (~df["qualified"]).sum())

print("\nPrioritätsverteilung:")
print(df["priority"].value_counts())

print("\nTop 10 Hotels:")
print(
    df[
        ["hotel_name", "region", "lead_score", "priority"]
    ].head(10).to_string(index=False)
)
