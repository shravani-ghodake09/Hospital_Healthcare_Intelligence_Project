
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Hospital Healthcare Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MODERN UI THEME
# ==========================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4f7ff, #eef7ff, #f8f5ff);
    color: #172554;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1 {
    color: #172554 !important;
    font-weight: 850 !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #263b80 !important;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172554, #312e81, #4338ca);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] input {
    color: #172554 !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #eef4ff);
    border: 1px solid #dbeafe;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(49, 46, 129, 0.09);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(49, 46, 129, 0.16);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 14px !important;
    font-weight: 650 !important;
}

div[data-testid="stMetricValue"] {
    color: #4338ca !important;
    font-weight: 850 !important;
    font-size: 27px !important;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #e0e7ff;
    border-radius: 18px;
    padding: 12px;
    box-shadow: 0 6px 22px rgba(30, 41, 59, 0.07);
    margin-bottom: 18px;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 16px;
    padding: 10px;
    box-shadow: 0 5px 20px rgba(30, 41, 59, 0.06);
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

hr {
    border-color: #c7d2fe;
}

.stCaption {
    color: #64748b;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    div[data-testid="stMetric"] {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.title("Hospital Healthcare Intelligence Dashboard")
st.caption(
    "Interactive analysis of hospital patients, departments, "
    "diagnoses, billing, insurance, satisfaction and outcomes."
)

st.divider()

# ==========================================
# LOAD DATASET
# ==========================================
DATA_FILE = Path(__file__).parent / "Hospital_Healthcare_Data.csv"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_FILE)
    data.columns = data.columns.str.strip()
    return data


try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load dataset: {e}")
    st.stop()

if df.empty:
    st.warning("The dataset contains no records.")
    st.stop()

# ==========================================
# COLOR PALETTE
# ==========================================
COLORS = [
    "#6366F1",
    "#06B6D4",
    "#F97316",
    "#10B981",
    "#EC4899",
    "#8B5CF6",
    "#F59E0B",
    "#14B8A6",
    "#EF4444",
    "#3B82F6",
    "#84CC16",
    "#D946EF"
]

PLOT_TEMPLATE = "plotly_white"


def style_figure(fig, height=420):
    """Apply consistent styling to Plotly charts."""
    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=height,
        title_x=0.02,
        title_font=dict(size=19, color="#172554"),
        font=dict(
            family="Arial, sans-serif",
            color="#334155",
            size=12
        ),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        margin=dict(l=20, r=20, t=65, b=35),
        hoverlabel=dict(
            bgcolor="#172554",
            font_size=13,
            font_color="white"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#cbd5e1",
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor="#e2e8f0",
        zeroline=False
    )

    return fig


def show_chart(fig, key):
    """Render a Plotly chart with interactive toolbar."""
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "responsive": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": key,
                "scale": 2
            }
        },
        key=key
    )


# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Customize the data displayed below.")

filtered_df = df.copy()

filter_columns = [
    ("Department", "Department"),
    ("Patient_Type", "Patient Type"),
    ("Gender", "Gender"),
    ("Room_Type", "Room Type"),
    ("Insurance", "Insurance")
]

for column, label in filter_columns:
    if column in filtered_df.columns:
        options = sorted(
            filtered_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            label,
            options,
            default=options,
            key=f"filter_{column}"
        )

        # Empty selection means no records for this filter.
        filtered_df = filtered_df[
            filtered_df[column].astype(str).isin(selected)
        ]

if filtered_df.empty:
    st.warning("No records match these filters.")
    st.stop()

st.sidebar.divider()
st.sidebar.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} records"
)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def find_column(possible_names, data=None):
    """Find the first matching column name."""
    source = data if data is not None else filtered_df

    for name in possible_names:
        if name in source.columns:
            return name

    return None


def numeric_column(possible_names):
    """Return a numeric Series, safely handling missing columns."""
    column = find_column(possible_names)

    if column:
        return pd.to_numeric(
            filtered_df[column],
            errors="coerce"
        )

    return pd.Series(index=filtered_df.index, dtype=float)


def count_data(column):
    """Count values in a categorical column."""
    if column not in filtered_df.columns:
        return None

    result = (
        filtered_df[column]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .rename_axis(column)
        .reset_index(name="Count")
    )

    return result


# ==========================================
# KPI CALCULATIONS
# ==========================================
billing = numeric_column(
    ["Billing_Amount", "Billing", "Bill_Amount"]
)

stay = numeric_column(
    ["Length_of_Stay", "Stay_Days", "Length_of_Stay_Days"]
)

rating = numeric_column(
    ["Satisfaction_Rating", "Rating", "Patient_Rating"]
)

total_patients = len(filtered_df)
total_billing = billing.sum()
avg_bill = billing.mean()
avg_stay = stay.mean()
avg_rating = rating.mean()

# ==========================================
# KPI CARDS
# ==========================================
st.subheader("Hospital Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Patients",
    f"{total_patients:,}"
)

c2.metric(
    "Total Billing",
    f"Rs. {total_billing:,.0f}"
)

c3.metric(
    "Average Bill",
    f"Rs. {avg_bill:,.0f}" if pd.notna(avg_bill) else "N/A"
)

c4.metric(
    "Average Stay",
    f"{avg_stay:.1f} days" if pd.notna(avg_stay) else "N/A"
)

c5.metric(
    "Average Rating",
    f"{avg_rating:.2f}/5" if pd.notna(avg_rating) else "N/A"
)

st.divider()

# ==========================================
# DEPARTMENT ANALYSIS
# ==========================================
st.header("Department Analysis")
st.caption("Explore patient distribution across hospital departments.")

department_data = count_data("Department")

if department_data is not None:
    fig = px.bar(
        department_data,
        x="Department",
        y="Count",
        color="Department",
        color_discrete_sequence=COLORS,
        title="Patients by Department",
        text="Count",
        hover_data={"Count": True, "Department": True}
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Patients: %{y:,}<extra></extra>"
        )
    )

    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Number of Patients")
    fig.update_xaxes(title="Department")

    show_chart(style_figure(fig), "department_chart")

# ==========================================
# PATIENT DEMOGRAPHICS
# ==========================================
st.header("Patient Demographics")

left, right = st.columns(2)

with left:
    gender_data = count_data("Gender")

    if gender_data is not None:
        fig = px.pie(
            gender_data,
            names="Gender",
            values="Count",
            hole=0.48,
            color_discrete_sequence=COLORS,
            title="Gender Distribution",
            hover_data=["Count"]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Patients: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )

        show_chart(style_figure(fig), "gender_donut")

with right:
    patient_type_data = count_data("Patient_Type")

    if patient_type_data is not None:
        fig = px.pie(
            patient_type_data,
            names="Patient_Type",
            values="Count",
            hole=0.48,
            color_discrete_sequence=COLORS,
            title="Patient Type Distribution",
            hover_data=["Count"]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Patients: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )

        show_chart(style_figure(fig), "patient_type_donut")

# ==========================================
# ROOM AND INSURANCE
# ==========================================
st.header("Room and Insurance Analysis")

left, right = st.columns(2)

with left:
    room_data = count_data("Room_Type")

    if room_data is not None:
        fig = px.bar(
            room_data,
            x="Room_Type",
            y="Count",
            color="Room_Type",
            color_discrete_sequence=COLORS,
            title="Patients by Room Type",
            text="Count"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Patients: %{y:,}<extra></extra>"
            )
        )

        fig.update_layout(showlegend=False)
        fig.update_yaxes(title="Number of Patients")
        fig.update_xaxes(title="Room Type")

        show_chart(style_figure(fig), "room_type_chart")

with right:
    insurance_data = count_data("Insurance")

    if insurance_data is not None:
        fig = px.pie(
            insurance_data,
            names="Insurance",
            values="Count",
            hole=0.45,
            color_discrete_sequence=COLORS,
            title="Insurance Distribution",
            hover_data=["Count"]
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Patients: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )

        show_chart(style_figure(fig), "insurance_donut")

# ==========================================
# DIAGNOSIS AND PAYMENT
# ==========================================
st.header("Diagnosis and Payment Analysis")

left, right = st.columns(2)

with left:
    diagnosis_data = count_data("Diagnosis")

    if diagnosis_data is not None:
        diagnosis_data = diagnosis_data.head(12)

        fig = px.bar(
            diagnosis_data.sort_values("Count"),
            x="Count",
            y="Diagnosis",
            orientation="h",
            color="Count",
            color_continuous_scale="Turbo",
            title="Most Common Diagnoses",
            text="Count"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Patients: %{x:,}<extra></extra>"
            )
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis_title="Diagnosis",
            xaxis_title="Number of Patients"
        )

        show_chart(style_figure(fig, 480), "diagnosis_chart")

with right:
    payment_data = count_data("Payment_Method")

    if payment_data is not None:
        fig = px.bar(
            payment_data,
            x="Payment_Method",
            y="Count",
            color="Payment_Method",
            color_discrete_sequence=COLORS,
            title="Patients by Payment Method",
            text="Count"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Patients: %{y:,}<extra></extra>"
            )
        )

        fig.update_layout(showlegend=False)
        fig.update_yaxes(title="Number of Patients")
        fig.update_xaxes(title="Payment Method")

        show_chart(style_figure(fig), "payment_chart")

# ==========================================
# ADMISSION TRENDS
# ==========================================
date_column = find_column([
    "Admission_Date",
    "Date_of_Admission",
    "AdmissionDate"
])

if date_column:
    st.header("Admission Trends")

    dates = pd.to_datetime(
        filtered_df[date_column],
        errors="coerce"
    )

    valid_dates = dates.dropna()

    if not valid_dates.empty:
        trend_data = (
            valid_dates
            .dt.to_period("M")
            .astype(str)
            .value_counts()
            .sort_index()
            .rename_axis("Month")
            .reset_index(name="Admissions")
        )

        fig = px.line(
            trend_data,
            x="Month",
            y="Admissions",
            markers=True,
            title="Monthly Admissions Over Time",
            color_discrete_sequence=["#6366F1"],
            hover_data={"Month": True, "Admissions": True}
        )

        fig.update_traces(
            line=dict(width=4),
            marker=dict(size=9),
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.12)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Admissions: %{y:,}<extra></extra>"
            )
        )

        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="Number of Admissions")

        show_chart(style_figure(fig), "admission_trend")
    else:
        st.info("No valid admission dates were found.")

# ==========================================
# BILLING ANALYSIS
# ==========================================
billing_column = find_column([
    "Billing_Amount",
    "Billing",
    "Bill_Amount"
])

if billing_column and "Department" in filtered_df.columns:
    st.header("Billing Analysis")

    bill_data = filtered_df[
        ["Department", billing_column]
    ].copy()

    bill_data[billing_column] = pd.to_numeric(
        bill_data[billing_column],
        errors="coerce"
    )

    bill_data = bill_data.dropna(
        subset=[billing_column]
    )

    bill_data = (
        bill_data
        .groupby("Department", as_index=False)[billing_column]
        .sum()
        .sort_values(billing_column, ascending=False)
    )

    if not bill_data.empty:
        fig = px.bar(
            bill_data,
            x="Department",
            y=billing_column,
            color="Department",
            color_discrete_sequence=COLORS,
            title="Total Billing by Department",
            text_auto=".2s",
            hover_data={billing_column: ":,.2f"}
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Total Billing: Rs. %{y:,.2f}<extra></extra>"
            )
        )

        fig.update_layout(showlegend=False)
        fig.update_yaxes(title="Total Billing (Rs.)")
        fig.update_xaxes(title="Department")

        show_chart(style_figure(fig, 470), "billing_chart")

# ==========================================
# OPTIONAL: LENGTH OF STAY
# ==========================================
stay_column = find_column([
    "Length_of_Stay",
    "Stay_Days",
    "Length_of_Stay_Days"
])

if stay_column and "Department" in filtered_df.columns:
    st.header("Length of Stay Analysis")

    stay_data = filtered_df[
        ["Department", stay_column]
    ].copy()

    stay_data[stay_column] = pd.to_numeric(
        stay_data[stay_column],
        errors="coerce"
    )

    stay_data = stay_data.dropna(
        subset=[stay_column]
    )

    if not stay_data.empty:
        stay_summary = (
            stay_data
            .groupby("Department", as_index=False)[stay_column]
            .mean()
            .sort_values(stay_column, ascending=False)
        )

        fig = px.bar(
            stay_summary,
            x="Department",
            y=stay_column,
            color="Department",
            color_discrete_sequence=COLORS,
            title="Average Length of Stay by Department",
            text_auto=".2f"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average Stay: %{y:.2f} days<extra></extra>"
            )
        )

        fig.update_layout(showlegend=False)
        fig.update_yaxes(title="Average Stay (Days)")
        fig.update_xaxes(title="Department")

        show_chart(style_figure(fig), "length_of_stay_chart")

# ==========================================
# PATIENT DATA TABLE
# ==========================================
st.header("Patient Data")
st.caption("Explore the filtered records below.")

search_text = st.text_input(
    "Search patient data",
    placeholder="Type a value to search across the table..."
)

table_df = filtered_df.copy()

if search_text.strip():
    mask = table_df.astype(str).apply(
        lambda column: column.str.contains(
            search_text,
            case=False,
            na=False,
            regex=False
        )
    ).any(axis=1)

    table_df = table_df[mask]

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Displaying {len(table_df):,} records "
    f"from {len(filtered_df):,} filtered records."
)

# ==========================================
# FOOTER
# ==========================================
st.divider()

st.caption(
    "Hospital Healthcare Intelligence Dashboard | "
    "Educational data analysis project. "
    "The dataset may contain synthetic records."
)