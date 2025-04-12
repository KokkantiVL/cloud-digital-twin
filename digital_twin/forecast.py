import pandas as pd
import psycopg2
from prophet import Prophet

# Connect to your local Postgres database
conn = psycopg2.connect(
    dbname="digital_twin_db",
    user="postgres",
    password="Lohi#70133",
    host="localhost",
    port="5432"
)

# Load sales data aggregated by date
query = """
SELECT date, SUM(sales) AS total_sales
FROM daily_store_summary
GROUP BY date
ORDER BY date;
"""

df = pd.read_sql(query, conn)
conn.close()

# Prepare data for Prophet
df_prophet = df.rename(columns={"date": "ds", "total_sales": "y"})

# Initialize and train the Prophet model
model = Prophet()
model.fit(df_prophet)

# Forecast the next 7 days
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

# Print the last 14 days (actual + forecast)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(14))