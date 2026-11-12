import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date
from lead_scoring import score_hotels
from sales_actions import generate_sales_actions

# 1. Seiteneinstellungen
st.set_page_config(
    page_title="Travelcircus Sales Intelligence",
    page_icon="📊",
    layout="wide"
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAFAFA;
    }

    h1, h2, h3 {
        color: #222222;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-left: 4px solid #C9243F;
        border-radius: 10px;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("data/scored_hotels.csv")
    df["follow_up_date"] = pd.to_datetime(
        df["follow_up_date"]
    )
    return df

# Datenquelle auswählen
st.sidebar.header("Datenquelle")

data_source = st.sidebar.radio(
    "Welche Hoteldaten möchtest du verwenden?",
    ["Demo-Daten", "Eigene Datei hochladen"]
)

if data_source == "Eigene Datei hochladen":

    uploaded_file = st.sidebar.file_uploader(
        "Excel- oder CSV-Datei auswählen",
        type=["xlsx", "csv"]
    )

    if uploaded_file is None:
        st.info("Bitte lade eine Excel- oder CSV-Datei hoch.")
        st.stop()

    # Datei einlesen
    try:
        if uploaded_file.name.lower().endswith(".xlsx"):
            raw_df = pd.read_excel(uploaded_file)
        else:
            raw_df = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(f"Die Datei konnte nicht gelesen werden: {error}")
        st.stop()

    # Erforderliche Spalten prüfen
    required_columns = [
        "hotel_name",
        "region",
        "google_rating",
        "rooms",
        "pool",
        "wellness_score",
        "image_score",
        "demand_score",
        "status",
        "owner",
        "follow_up_date",
        "potential_revenue"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in raw_df.columns
    ]

    if missing_columns:
        st.error(
            "Diese Spalten fehlen in deiner Datei: "
            + ", ".join(missing_columns)
        )
        st.stop()

    # Datenformate überprüfen und vereinheitlichen
    try:
        numeric_columns = [
            "google_rating",
            "rooms",
            "wellness_score",
            "image_score",
            "demand_score",
            "potential_revenue"
        ]

        for column in numeric_columns:
            raw_df[column] = pd.to_numeric(
                raw_df[column],
                errors="raise"
            )

        raw_df["pool"] = (
            raw_df["pool"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "true": True,
                "false": False,
                "ja": True,
                "nein": False,
                "1": True,
                "0": False
            })
        )

        if raw_df["pool"].isna().any():
            raise ValueError(
                "Die Spalte 'pool' muss Ja/Nein oder True/False enthalten."
            )

        raw_df["follow_up_date"] = pd.to_datetime(
            raw_df["follow_up_date"],
            errors="raise"
        )

        if raw_df.empty:
            raise ValueError("Die Datei enthält keine Hotels.")

        # Hotels automatisch bewerten
        df = score_hotels(raw_df)

    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Ungültige Hoteldaten: {error}")
        st.stop()

    st.sidebar.success(
        f"{len(df)} Hotels erfolgreich eingelesen und bewertet!"
    )

else:
    # Bisherige Demo-Daten verwenden
    df = load_data()


df["follow_up_display"] = df["follow_up_date"].dt.strftime("%d.%m.%Y")

# 3. Überschrift
st.title("📊 Travelcircus Sales Intelligence")
st.caption(
    "Lead Scoring & Sales Pipeline Monitoring | "
    "Demo mit fiktiven Hoteldaten"
)

# 4. Filter in der Seitenleiste
st.sidebar.header("Filter")

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

selected_priorities = st.sidebar.multiselect(
    "Priorität",
    options=["A", "B", "C", "Nicht qualifiziert"],
    default=["A", "B", "C", "Nicht qualifiziert"]
)

filtered_df = df[
    df["region"].isin(selected_regions)
    & df["priority"].isin(selected_priorities)
].copy()

# 5. KPI-Berechnungen
today = pd.Timestamp(date.today())

overdue_mask = (
    (filtered_df["follow_up_date"] < today)
    & (filtered_df["status"] != "Gewonnen")
)

total_leads = len(filtered_df)
qualified_leads = filtered_df["qualified"].sum()
top_leads = (filtered_df["priority"] == "A").sum()
overdue_leads = overdue_mask.sum()

# 6. KPI-Karten anzeigen
col1, col2, col3, col4 = st.columns(4)

col1.metric("Hotel-Leads", total_leads)
col2.metric("Qualifiziert", int(qualified_leads))
col3.metric("A-Leads", int(top_leads))
col4.metric("Überfällige Follow-ups", int(overdue_leads))

st.divider()

# 7. Diagramme
left, right = st.columns(2)

with left:
    st.subheader("Lead-Prioritäten")

    priority_counts = (
        filtered_df["priority"]
        .value_counts()
        .reset_index()
    )
    priority_counts.columns = ["priority", "count"]

    fig_priority = px.bar(
        priority_counts,
        x="priority",
        y="count",
        color="priority",
        title="Verteilung nach Priorität"
    )

    st.plotly_chart(fig_priority, use_container_width=True)

with right:
    st.subheader("Sales Pipeline")

    status_counts = (
        filtered_df["status"]
        .value_counts()
        .reset_index()
    )
    status_counts.columns = ["status", "count"]

    fig_pipeline = px.bar(
        status_counts,
        x="status",
        y="count",
        title="Leads nach Sales-Status"
    )

    st.plotly_chart(fig_pipeline, use_container_width=True)

st.divider()

# 8. Lead-Ranking
st.subheader("🏆 Hotel Lead Ranking")

ranking_columns = [
    "hotel_name",
    "region",
    "google_rating",
    "rooms",
    "lead_score",
    "priority",
    "status",
    "owner"
]

st.dataframe(
    filtered_df[ranking_columns],
    use_container_width=True,
    hide_index=True
)

# 9. Überfällige Follow-ups
st.subheader("⚠️ Überfällige Follow-ups")

overdue_df = filtered_df[overdue_mask].sort_values(
    "follow_up_date"
)

if overdue_df.empty:
    st.success("Keine überfälligen Follow-ups vorhanden.")
else:
    st.warning(
        f"{len(overdue_df)} Leads benötigen Aufmerksamkeit."
    )

    st.dataframe(
        overdue_df[
            [
                "hotel_name",
                "owner",
                "status",
                "follow_up_display",
                "priority"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# 10. CSV-Export
st.divider()

st.download_button(
    label="📥 Gefilterte Leads als CSV herunterladen",
    data=filtered_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="travelcircus_leads_export.csv",
    mime="text/csv"
)

# 11. Sales Action Center
st.divider()
st.subheader("🚨 Sales Action Center")

st.caption(
    "Automatische Handlungsempfehlungen auf Basis "
    "definierter Geschäftsregeln."
)

actions_df = generate_sales_actions(filtered_df)

if not actions_df.empty:
    actions_df["follow_up_display"] = pd.to_datetime(
        actions_df["follow_up_date"]
    ).dt.strftime("%d.%m.%Y")

if actions_df.empty:
    st.info("Keine offenen Sales-Aktionen vorhanden.")

else:
    critical_actions = (
        actions_df["action_priority"] == "Kritisch"
    ).sum()

    high_actions = (
        actions_df["action_priority"] == "Hoch"
    ).sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Kritische Aktionen",
        int(critical_actions)
    )

    col2.metric(
        "Hohe Priorität",
        int(high_actions)
    )

    action_filter = st.multiselect(
        "Dringlichkeit auswählen",
        ["Kritisch", "Hoch", "Mittel", "Normal"],
        default=["Kritisch", "Hoch", "Mittel"]
    )

    visible_actions = actions_df[
        actions_df["action_priority"].isin(action_filter)
    ]

    st.dataframe(
        visible_actions[
            [
                "hotel_name",
                "owner",
                "lead_priority",
                "action_priority",
                "reason",
                "recommended_action",
                "follow_up_display"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
