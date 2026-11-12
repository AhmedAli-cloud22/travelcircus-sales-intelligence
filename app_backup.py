import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date

# 1. Seiteneinstellungen
st.set_page_config(
    page_title="Travelcircus Sales Intelligence",
    page_icon="📊",
    layout="wide"
)

# 2. Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("data/scored_hotels.csv")
    df["follow_up_date"] = pd.to_datetime(
        df["follow_up_date"]
    )
    return df

df = load_data()

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
                "follow_up_date",
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
