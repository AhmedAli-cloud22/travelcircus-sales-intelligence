import pandas as pd


def generate_sales_actions(df):
    today = pd.Timestamp.today().normalize()

    actions = []

    for _, hotel in df.iterrows():

        # Nicht qualifizierte Hotels überspringen
        if not hotel["qualified"]:
            continue

        # Bereits gewonnene Deals überspringen
        if hotel["status"] == "Gewonnen":
            continue

        hotel_name = hotel["hotel_name"]
        owner = hotel["owner"]
        status = hotel["status"]
        follow_up = pd.to_datetime(hotel["follow_up_date"])

        days_overdue = (today - follow_up).days

         # Regel 1: Überfälliges Angebot
        if status == "Angebot angefragt" and days_overdue > 0:
            priority = "Kritisch"
            reason = f"Angebot seit {days_overdue} Tagen überfällig"

            if owner == "Nicht zugewiesen":
                action = (
                    "Sofort Sales Manager zuweisen und "
                    "Angebotsstatus klären."
                )
            else:
                action = (
                    "Angebotsstatus prüfen und Hotel "
                    "zeitnah kontaktieren."
                )

        # Regel 2: Fehlender Verantwortlicher
        elif owner == "Nicht zugewiesen":
            priority = "Hoch"
            reason = "Kein Verantwortlicher zugewiesen"
            action = "Sales Manager zuweisen und Kontakt planen."

        # Regel 3: Anderer überfälliger Follow-up
        elif days_overdue > 0:
            priority = "Hoch"
            reason = f"Follow-up {days_overdue} Tage überfällig"
            action = "Follow-up durchführen und CRM aktualisieren."

        # Regel 4: Heute fällig
        elif days_overdue == 0:
            priority = "Mittel"
            reason = "Follow-up heute fällig"
            action = "Heute Kontakt aufnehmen."

        # Regel 5: Kein akuter Handlungsbedarf
        else:
            priority = "Normal"
            reason = "Kein überfälliger Termin"
            action = "Nächsten Termin im CRM überwachen."


        actions.append({
            "hotel_name": hotel_name,
            "owner": owner,
            "status": status,
            "lead_score": hotel["lead_score"],
            "lead_priority": hotel["priority"],
            "action_priority": priority,
            "reason": reason,
            "recommended_action": action,
            "follow_up_date": follow_up.date()
        })

    result = pd.DataFrame(actions)

    if result.empty:
        return result

    priority_order = {
        "Kritisch": 0,
        "Hoch": 1,
        "Mittel": 2,
        "Normal": 3
    }

    result["sort_order"] = result["action_priority"].map(
        priority_order
    )

    result = result.sort_values(
        by=["sort_order", "lead_score"],
        ascending=[True, False]
    )

    return result.drop(columns=["sort_order"])
