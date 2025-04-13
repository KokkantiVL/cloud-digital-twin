import streamlit as st
import pandas as pd
import psycopg2
from prophet import Prophet

st.title("📦 Digital Twin Dashboard for Retail Analytics")

# Connect to DB
conn = psycopg2.connect(
    dbname="digital_twin_db",
    user="postgres",
    password="Lohi123",
    host="localhost",
    port="5432"
)

# Load daily store summary
query = """
SELECT date, SUM(sales) as total_sales
FROM daily_store_summary
GROUP BY date
ORDER BY date
"""
df = pd.read_sql(query, conn)

# Prophet Forecast
df_prophet = df.rename(columns={"date": "ds", "total_sales": "y"})
model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

# Plot forecast
st.subheader("📈 7-Day Sales Forecast")
fig1 = model.plot(forecast)
st.pyplot(fig1)

# Inventory Simulation
st.subheader("🔁 Inventory Simulation (Basic)")
starting_inventory = st.number_input("Starting Inventory", value=1000)
avg_shipment = st.number_input("Daily Shipment Quantity", value=87)

inventory = [starting_inventory]
for i in range(7):
    sales = forecast.iloc[-7 + i]['yhat']
    new_level = inventory[-1] + avg_shipment - sales
    inventory.append(new_level)

sim_df = pd.DataFrame({
    "Day": [f"Day {i+1}" for i in range(7)],
    "Forecasted Sales": forecast['yhat'].tail(7).astype(int).values,
    "Shipment": [avg_shipment] * 7,
    "Inventory Level": inventory[1:]
})

st.dataframe(sim_df)

# Clean up
conn.close()
