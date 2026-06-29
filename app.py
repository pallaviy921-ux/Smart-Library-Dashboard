import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interactive Dashboard")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_library_dataset.csv")   # Change filename if needed
    return df

df = load_data()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

columns = df.select_dtypes(include='object').columns

for col in columns:
    options = st.sidebar.multiselect(
        f"Select {col}",
        df[col].unique(),
        default=df[col].unique()
    )
    df = df[df[col].isin(options)]

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    missing = df.isnull().sum().sum()
    st.metric("Missing Values", missing)

st.divider()

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(df)

# -----------------------------
# Charts
# -----------------------------
numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
categorical_cols = df.select_dtypes(include='object').columns.tolist()

if len(categorical_cols) > 0 and len(numeric_cols) > 0:

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Bar Chart")

        x = st.selectbox("Select Category", categorical_cols)

        y = st.selectbox("Select Numeric", numeric_cols)

        fig = px.bar(
            df,
            x=x,
            y=y,
            color=x
        )

        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Pie Chart")

        pie = px.pie(
            df,
            names=x
        )

        st.plotly_chart(pie, use_container_width=True)

# -----------------------------
# Line Chart
# -----------------------------
if len(numeric_cols) > 0:

    st.subheader("Line Chart")

    line_col = st.selectbox(
        "Choose Numeric Column",
        numeric_cols,
        key="line"
    )

    fig = px.line(df, y=line_col)

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Histogram
# -----------------------------
if len(numeric_cols) > 0:

    st.subheader("Histogram")

    hist = st.selectbox(
        "Histogram Column",
        numeric_cols,
        key="hist"
    )

    fig = px.histogram(df, x=hist)

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation Heatmap
# -----------------------------
if len(numeric_cols) > 1:

    st.subheader("Correlation Matrix")

    corr = df[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Download Button
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)