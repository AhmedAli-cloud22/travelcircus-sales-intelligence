import pandas as pd
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

regions = [
    "Allgäu", "Chiemgau", "Bayerischer Wald",
    "Oberbayern", "Franken", "Berchtesgadener Land"
]

statuses = [
    "Neu", "Kontaktiert", "Interessiert",
    "Angebot angefragt", "Verhandlung", "Gewonnen"
]

owners = ["Anna", "Max", "Sophie", "Leon", "Nicht zugewiesen"]

hotels = []

for i in range(1, 61):
    status = random.choice(statuses)
    owner = random.choice(owners)

    hotels.append({
        "hotel_id": i,
        "hotel_name": f"Demo Wellnesshotel {i:02d}",
        "region": random.choice(regions),
        "google_rating": round(random.uniform(3.5, 5.0), 1),
        "rooms": random.randint(20, 180),
        "pool": random.choice([True, False]),
        "wellness_score": random.randint(1, 5),
        "image_score": random.randint(1, 5),
        "demand_score": random.randint(1, 5),
        "deal_score": random.randint(1, 5),
        "status": status,
        "owner": owner,
        "potential_revenue": random.randrange(3000, 30001, 500),
        "follow_up_date": (
            date.today() + timedelta(days=random.randint(-10, 14))
        ).isoformat()
    })

df = pd.DataFrame(hotels)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/hotels.csv", index=False)

print("60 Demo-Hotels erfolgreich erstellt!")
print(df.head().to_string(index=False))
