import psycopg2
import pandas as pd
from prophet import Prophet

# Connect to Postgres
conn = psycopg2.connect(
    dbname="digital_twin_db",
    user="postgres",
    password="Lohi#70133",
    host="localhost",
    port="5432"
)

# Get historical sales summary
query = """
SELECT date, SUM(sales) AS total_sales
FROM daily_store_summary
GROUP BY date
ORDER BY date
"""
df = pd.read_sql(query, conn)

# Forecast next 7 days of sales
df_prophet = df.rename(columns={"date": "ds", "total_sales": "y"})
model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)
forecast = forecast[['ds', 'yhat']].tail(7)

# Get incoming shipments (use last week's average if forecast period exceeds table)
supply_query = """
SELECT date, SUM(shipment_arrivals) AS total_shipments
FROM supply_chain
GROUP BY date
ORDER BY date DESC
LIMIT 7
"""
supply_df = pd.read_sql(supply_query, conn)
conn.close()

avg_shipments = int(supply_df['total_shipments'].mean())
shipments = [avg_shipments] * 7

# Start inventory simulation
current_inventory = 1000
print(f"Starting Inventory: {current_inventory}")
print("Simulating next 7 days:\n")

for i in range(7):
    forecasted_sales = int(forecast.iloc[i]['yhat'])
    shipment = shipments[i]
    new_inventory = current_inventory + shipment - forecasted_sales
    print(f"Day {i+1}: Forecasted Sales = {forecasted_sales}, Shipment = {shipment}, New Inventory = {new_inventory}")
    current_inventory = new_inventory