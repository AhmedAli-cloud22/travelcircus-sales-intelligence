import pandas as pd
from datetime import date, timedelta
from sales_actions import generate_sales_actions

# Ein fiktives Hotel für unseren Test erstellen
test_hotel = pd.DataFrame([{
    "hotel_name": "Test Wellness Resort",
    "qualified": True,
    "status": "Angebot angefragt",
    "owner": "Anna",
    "lead_score": 90,
    "priority": "A",
    "follow_up_date": date.today() - timedelta(days=5)
}])

# Unsere Funktion mit den Testdaten aufrufen
result = generate_sales_actions(test_hotel)

# Prüfen, ob das Ergebnis korrekt ist
assert len(result) == 1
assert result.iloc[0]["action_priority"] == "Kritisch"

print("Test bestanden! Überfälliges Angebot wird korrekt erkannt.")

# TEST 2: Hotel ohne Sales Manager
hotel_no_owner = test_hotel.copy()
hotel_no_owner["owner"] = "Nicht zugewiesen"
hotel_no_owner["status"] = "Interessiert"

result = generate_sales_actions(hotel_no_owner)

assert result.iloc[0]["action_priority"] == "Hoch"
print("Test 2 bestanden: Fehlender Owner erkannt.")


# TEST 3: Bereits gewonnener Deal
hotel_won = test_hotel.copy()
hotel_won["status"] = "Gewonnen"

result = generate_sales_actions(hotel_won)

assert result.empty
print("Test 3 bestanden: Gewonnener Deal übersprungen.")


# TEST 4: Nicht qualifiziertes Hotel
hotel_unqualified = test_hotel.copy()
hotel_unqualified["qualified"] = False

result = generate_sales_actions(hotel_unqualified)

assert result.empty
print("Test 4 bestanden: Nicht qualifiziertes Hotel übersprungen.")

# TEST 5: Überfälliges Angebot ohne Owner
hotel_critical = test_hotel.copy()

hotel_critical["owner"] = "Nicht zugewiesen"
hotel_critical["status"] = "Angebot angefragt"

result = generate_sales_actions(hotel_critical)

assert result.iloc[0]["action_priority"] == "Kritisch"

assert "Sales Manager zuweisen" in (
    result.iloc[0]["recommended_action"]
)

print("Test 5 bestanden: Kritisches Angebot ohne Owner erkannt.")
