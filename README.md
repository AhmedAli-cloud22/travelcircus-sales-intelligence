# Travelcircus Sales Intelligence Dashboard

**Ein persönliches Praxisprojekt von Ahmed Ali**

## Warum ich dieses Projekt entwickelt habe

Im Rahmen meiner Bewerbung als Junior Business Analyst Sales bei Travelcircus wollte ich nicht nur über meine Fähigkeiten sprechen, sondern auch praktisch zeigen, wie ich an eine Aufgabe herangehe.

Ich habe Wirtschaftsinformatik studiert und interessiere mich besonders dafür, wie man Daten nutzen kann, um Geschäftsprozesse zu verbessern und Entscheidungen zu unterstützen.

Bei der Beschäftigung mit der Hotelakquise habe ich mir deshalb zwei Fragen gestellt:

- Wie könnte man potenzielle Hotelpartner systematisch bewerten und priorisieren?
- Wie könnte man Sales-Mitarbeitern helfen, den Überblick über ihre Leads und nächsten Aufgaben zu behalten?

Aus diesen Überlegungen ist dieses kleine Dashboard entstanden.

## Meine Idee

Ich wollte ein einfaches Tool entwickeln, das zwei Bereiche miteinander verbindet:

**1. Hotel Lead Scoring**

Nicht jedes Hotel ist automatisch ein gleich interessanter Partner. Deshalb habe ich ein Modell entwickelt, das Hotels anhand bestimmter Kriterien bewertet.

**2. Sales Action Center**

Ein guter Lead bringt wenig, wenn wichtige Follow-ups vergessen werden. Deshalb wollte ich zusätzlich sichtbar machen, welche Vertriebsaktivitäten gerade Aufmerksamkeit benötigen.

Beide Bereiche habe ich in einem interaktiven Dashboard zusammengeführt.

## Was das Dashboard kann

### Hotel Lead Scoring

Das System prüft zunächst, ob ein Hotel bestimmte Mindestanforderungen erfüllt:

| Kriterium | Mindestanforderung |
|-----------|-------------------|
| Google-Bewertung | Mindestens 4,0 |
| Zimmeranzahl | Mindestens 30 |
| Swimmingpool | Vorhanden |
| Wellness-Score | Mindestens 3 |

Erfüllt ein Hotel diese Kriterien, wird ein gewichteter Lead Score berechnet.

Dafür habe ich folgende Faktoren berücksichtigt:

| Faktor | Gewichtung |
|--------|------------|
| Wellness-Qualität | 30 % |
| Bildqualität | 25 % |
| Reputation | 20 % |
| Nachfragepotenzial | 15 % |
| Zimmerkapazität | 10 % |

Die Hotels werden anschließend in Prioritätsgruppen eingeteilt:

- **A:** Ab 80 Punkten
- **B:** Ab 60 Punkten
- **C:** Unter 60 Punkten
- **Nicht qualifiziert:** Mindestanforderungen nicht erfüllt

Die Kriterien und Gewichtungen sind meine eigenen beispielhaften Annahmen und keine offiziellen Regeln von Travelcircus.

### Sales Pipeline

Im Dashboard kann man sehen, in welcher Vertriebsphase sich die einzelnen Hotel-Leads befinden.

Dazu gehören beispielsweise:

- Neu
- Kontaktiert
- Interessiert
- Angebot angefragt
- Verhandlung
- Gewonnen

Zusätzlich lassen sich die Daten nach Region und Priorität filtern.

### Sales Action Center

Bei diesem Teil ging es mir darum, aus den Daten konkrete Handlungsempfehlungen abzuleiten.

Das System erkennt beispielsweise:

- Leads ohne zuständigen Mitarbeiter
- Überfällige Follow-ups
- Überfällige Angebote
- Aufgaben, die heute fällig sind

Je nach Situation wird eine Priorität vergeben und eine passende nächste Aktion vorgeschlagen.

So soll aus einer reinen Datenübersicht ein Werkzeug werden, das bei der täglichen Vertriebsarbeit unterstützt.

## Verwendete Technologien

| Technologie | Aufgabe |
|-------------|---------|
| Python | Programmierung und Geschäftslogik |
| Pandas | Datenverarbeitung und Analyse |
| Streamlit | Entwicklung des Dashboards |
| Plotly | Interaktive Diagramme |
| CSV / Excel | Datenhaltung und Testdaten |

## Projektstruktur

```text
travelcircus-sales-intelligence/
├── app.py
├── generate_data.py
├── scoring.py
├── sales_actions.py
├── create_test_hotels.py
├── requirements.txt
├── README.md
└── data/
    ├── hotels.csv
    ├── scored_hotels.csv
    └── test_hotels.xlsx
```

## Installation und Start

### 1. Repository herunterladen

```bash
git clone https://github.com/DEIN_USERNAME/travelcircus-sales-intelligence.git
cd travelcircus-sales-intelligence
```

### 2. Virtuelle Umgebung erstellen

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Pakete installieren

```bash
pip install -r requirements.txt
```

### 4. Beispieldaten generieren

```bash
python generate_data.py
python scoring.py
```

### 5. Dashboard starten

```bash
streamlit run app.py
```

Anschließend kann das Dashboard im Browser geöffnet werden.

## Was ich bei diesem Projekt gelernt habe

Für mich war dieses Projekt eine gute Gelegenheit, mein Wissen aus dem Wirtschaftsinformatikstudium praktisch einzusetzen.

Besonders interessant fand ich, dass es nicht nur darum geht, Daten zu visualisieren. Man muss sich vorher überlegen, welche Informationen für eine Entscheidung relevant sind und wie man daraus nachvollziehbare Regeln ableiten kann.

Ich habe dabei mit Python und Pandas Daten verarbeitet, eine Scoring-Logik umgesetzt und mit Streamlit ein interaktives Dashboard aufgebaut.

Außerdem habe ich mich damit beschäftigt, wie man aus einer Analyse konkrete nächste Schritte für den Vertrieb ableiten kann.

## Was ich noch verbessern würde

Das Dashboard ist ein erster Prototyp. Mit mehr Zeit und echten Daten würde ich gerne weitere Funktionen ergänzen:

- Anbindung an eine echte Hotel- oder CRM-Datenquelle
- Überprüfung der Scoring-Gewichtungen anhand tatsächlicher Vertriebsergebnisse
- Automatische Aktualisierung der Hotelinformationen
- Analyse von Conversion Rates je Vertriebsphase
- Erweiterte Auswertung des potenziellen Umsatzes

## Hinweis zu den Daten

Alle verwendeten Hotel- und Vertriebsdaten sind fiktiv und wurden ausschließlich für dieses Projekt erstellt.

Das Dashboard ist kein offizielles System von Travelcircus. Die verwendeten Kriterien und Regeln dienen dazu, meinen Lösungsansatz zu demonstrieren.

## Über mich

**Ahmed Ali**

Bachelorabschluss in Wirtschaftsinformatik

Mich interessiert besonders die Verbindung zwischen Datenanalyse, Geschäftsprozessen und praktischen Lösungen.

Mit diesem Projekt möchte ich zeigen, dass ich mich gerne selbstständig in neue Aufgaben einarbeite, analytisch denke und nicht nur Probleme beschreiben, sondern auch konkrete Lösungen entwickeln möchte.

---

*Entwickelt von Ahmed Ali als eigenständiges Praxisprojekt im Rahmen meiner Bewerbung bei Travelcircus.*





