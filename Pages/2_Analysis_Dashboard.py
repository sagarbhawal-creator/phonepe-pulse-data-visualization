import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.set_page_config(layout="wide")

st.title("📊 PhonePe Transaction Insights Dashboard")

# ---------------- DATABASE CONNECTION ---------------- #

conn = get_connection()

# ---------------- SIDEBAR FILTERS ---------------- #

st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    (2018, 2019, 2020, 2021, 2022, 2023)
)

quarter = st.sidebar.selectbox(
    "Select Quarter",
    (1, 2, 3, 4)
)

menu = st.sidebar.selectbox(
    "Select Business Case",
    [
        "Transaction Dynamics",
        "Device Dominance",
        "Insurance Growth",
        "Market Expansion",
        "User Growth"
    ]
)

# ---------------- KPI METRICS ---------------- #

st.subheader(f"📌 Overall Metrics — {year} Q{quarter}")

col1, col2, col3 = st.columns(3)

query1 = f"""
SELECT SUM(transaction_amount) AS total_txn
FROM aggregated_transactions
WHERE year={year} AND quarter={quarter}
"""

query2 = f"""
SELECT SUM(user_count) AS total_users
FROM aggregated_user
WHERE year={year} AND quarter={quarter}
"""

query3 = f"""
SELECT SUM(insurance_amount) AS total_insurance
FROM aggregated_insurance
WHERE year={year} AND quarter={quarter}
"""

df1 = pd.read_sql(query1, conn).fillna(0)
df2 = pd.read_sql(query2, conn).fillna(0)
df3 = pd.read_sql(query3, conn).fillna(0)

txn_cr = df1["total_txn"][0] / 10000000
insurance_cr = df3["total_insurance"][0] / 10000000

col1.metric("💰 Total Transactions", f"₹ {txn_cr:,.0f} Cr")
col2.metric("👥 Total Users", f"{int(df2['total_users'][0]):,}")
col3.metric("🛡 Total Insurance", f"₹ {insurance_cr:,.0f} Cr")

st.divider()

# ---------------- TOP STATES CHART ---------------- #

st.subheader(f"🏆 Top States by Transactions — {year} Q{quarter}")

query_states = f"""
SELECT state, SUM(transaction_amount) AS total
FROM aggregated_transactions
WHERE year={year} AND quarter={quarter}
GROUP BY state
ORDER BY total DESC
LIMIT 10
"""

df_states = pd.read_sql(query_states, conn)

df_states["total_cr"] = df_states["total"] / 10000000

fig_states = px.bar(
    df_states,
    x="state",
    y="total_cr",
    color="total_cr",
    color_continuous_scale="Purples"
)

fig_states.update_layout(
    xaxis_title="State",
    yaxis_title="Transaction Amount (₹ Cr)",
    xaxis_tickangle=-45
)

st.plotly_chart(fig_states, use_container_width=True)

st.divider()

# ---------------- BUSINESS CASES ---------------- #

# 1 Transaction Dynamics
if menu == "Transaction Dynamics":

    st.header("📈 Transaction Trend Over Years")

    query = """
    SELECT year, SUM(transaction_amount) AS total
    FROM aggregated_transactions
    GROUP BY year
    ORDER BY year
    """

    df = pd.read_sql(query, conn)

    df["total_cr"] = df["total"] / 10000000

    fig = px.line(df, x="year", y="total_cr", markers=True)

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Transaction Amount (₹ Cr)"
    )

    st.plotly_chart(fig, use_container_width=True)

# 2 Device Dominance
elif menu == "Device Dominance":

    st.header(f"📱 Top Mobile Brands — {year} Q{quarter}")

    query = f"""
    SELECT brand, SUM(user_count) AS users
    FROM aggregated_user
    WHERE year={year} AND quarter={quarter}
    GROUP BY brand
    ORDER BY users DESC
    LIMIT 10
    """

    df = pd.read_sql(query, conn)

    fig = px.pie(
        df,
        names="brand",
        values="users"
    )

    st.plotly_chart(fig, use_container_width=True)

# 3 Insurance Growth
elif menu == "Insurance Growth":

    st.header("🛡 Insurance Growth Over Years")

    query = """
    SELECT year, SUM(insurance_amount) AS total
    FROM aggregated_insurance
    GROUP BY year
    ORDER BY year
    """

    df = pd.read_sql(query, conn)

    df["total_cr"] = df["total"] / 10000000

    fig = px.line(df, x="year", y="total_cr", markers=True)

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Insurance Amount (₹ Cr)"
    )

    st.plotly_chart(fig, use_container_width=True)

# 4️ Market Expansion
elif menu == "Market Expansion":

    st.header(f"🌍 Top District Transactions — {year} Q{quarter}")

    query = f"""
    SELECT district, SUM(transaction_amount) AS total
    FROM map_transaction
    WHERE year={year} AND quarter={quarter}
    GROUP BY district
    ORDER BY total DESC
    LIMIT 10
    """

    df = pd.read_sql(query, conn)

    df["total_cr"] = df["total"] / 10000000

    fig = px.bar(
        df,
        x="district",
        y="total_cr",
        color="total_cr",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        xaxis_title="District",
        yaxis_title="Transaction Amount (₹ Cr)",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

# 5️ User Growth
elif menu == "User Growth":

    st.header(f"👥 Top Pincodes by Registered Users — {year} Q{quarter}")

    query = f"""
    SELECT pincode, SUM(registered_users) AS users
    FROM top_user
    WHERE year={year} AND quarter={quarter}
    GROUP BY pincode
    ORDER BY users DESC
    LIMIT 10
    """

    df = pd.read_sql(query, conn)

    fig = px.bar(
        df,
        x="pincode",
        y="users",
        color="users",
        color_continuous_scale="Oranges"
    )

    fig.update_layout(
        xaxis_title="Pincode",
        yaxis_title="Total Users"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- CLOSE CONNECTION ---------------- #

conn.close()