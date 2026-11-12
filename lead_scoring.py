import pandas as pd


def score_hotels(df):
    # Kopie erstellen, damit die Originaldaten erhalten bleiben
    df = df.copy()

    # 1. Mindestanforderungen überprüfen
    df["qualified"] = (
        (df["google_rating"] >= 4.0)
        & (df["rooms"] >= 30)
        & (df["pool"] == True)
        & (df["wellness_score"] >= 3)
    )

    # 2. Kriterien auf 0 bis 100 Punkte skalieren
    df["wellness_points"] = df["wellness_score"] * 20
    df["image_points"] = df["image_score"] * 20
    df["reputation_points"] = df["google_rating"] * 20
    df["demand_points"] = df["demand_score"] * 20

    # 3. Zimmerkapazität bewerten
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

    # 6. Hotels sortieren
    df = df.sort_values(
        by=["qualified", "lead_score"],
        ascending=[False, False]
    )

    return df

