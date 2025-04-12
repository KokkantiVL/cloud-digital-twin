# Digital Twin Prototype (Local-Only)

Hey there! This project shows how to build a **Digital Twin** for a retail store — **all on your own computer** and without spending a dime on the cloud.

## Why This Is Cool

- **Zero Cloud Costs**: Everything runs on your local machine.
- **Full Workflow**: We go from CSV data → PostgreSQL → dbt transformations → Prophet forecasting → a live simulation script → and an interactive dashboard in Streamlit.
- **Super Flexible**: You can easily tweak numbers and see what happens (e.g., if shipments change).

---

## Project Overview

cloud-digital-twin/
├── digital_twin/                    # The main dbt project folder
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_store_operations.sql
│   │   │   └── stg_supply_chain.sql
│   │   └── analytics/
│   │       └── daily_store_summary.sql
│   ├── forecast.py                  # Prophet-based time-series forecast
│   ├── digital_twin_sim.py          # Daily inventory simulation
│   ├── dashboard.py                 # Streamlit for visual dashboards
├── store_operations.csv             # Synthetic sample data
├── supply_chain.csv                 # Synthetic sample data
└── README.md

1. **store_operations.csv**: Tracks sales, foot traffic, inventory.  
2. **supply_chain.csv**: Tracks incoming shipments and lead times.  
3. **dbt**: Cleans and transforms data into analytics-friendly tables.  
4. **Prophet**: Predicts next 7 days of sales.  
5. **digital_twin_sim**: Calculates day-by-day inventory levels based on shipments and forecasts.  
6. **Streamlit**: Lets you see everything in a friendly web-based dashboard.

---

## Setup Steps

### 1. Install Things

- [PostgreSQL](https://www.postgresql.org/download/)
- Python 3
- dbt with the Postgres adapter:
  ```bash
  pip install dbt-postgres

	•	Prophet, Streamlit, psycopg2, pandas:

pip install prophet streamlit psycopg2 pandas



2. Create a Local Database

Open a terminal and do:

psql -U postgres
CREATE DATABASE digital_twin_db;

3. Load the CSV Data

Inside psql:

\c digital_twin_db

CREATE TABLE store_operations (
  date DATE,
  store_id INT,
  sales INT,
  foot_traffic INT,
  inventory_level INT
);

CREATE TABLE supply_chain (
  date DATE,
  store_id INT,
  shipment_arrivals INT,
  lead_time_days INT,
  reorder_quantity INT
);

\copy store_operations(date, store_id, sales, foot_traffic, inventory_level)
FROM '/absolute/path/to/store_operations.csv' DELIMITER ',' CSV HEADER;

\copy supply_chain(date, store_id, shipment_arrivals, lead_time_days, reorder_quantity)
FROM '/absolute/path/to/supply_chain.csv' DELIMITER ',' CSV HEADER;

4. Run dbt

cd digital_twin
dbt run

This creates the transformed views so we can do analytics more easily.

5. Forecast Sales

python forecast.py

This script uses Prophet to predict the next 7 days of sales.

6. Simulate the Digital Twin

python digital_twin_sim.py

It calculates new inventory levels each day based on forecasted sales and average shipments. If you see negative numbers, it means you’re selling out too quickly!

7. View the Dashboard

streamlit run dashboard.py

Visit http://localhost:8501 in your browser. Play around with:
	•	Starting Inventory
	•	Daily Shipment Quantity
Watch your table and forecast chart update in real time.



Cool Things to Try
	1.	Up Shipment Quantities: Tweak your daily shipment to avoid stockouts.
	2.	Reduce Foot Traffic (in digital_twin_sim.py) to see if it solves negative inventory issues.
	3.	Add More Days: Extend the Prophet forecast to 14 days or 30 days.
	4.	Deploy: Host the dashboard on a cheap or free service (like Streamlit Cloud or Railway).


Troubleshooting

	•	CSV Not Found: Make sure you use absolute paths or open psql from the same folder.
	•	Negative Inventory: That’s actually a feature. It means shipments aren’t keeping up with demand.
	•	Prophet Complaints: On some systems, you might need to install extra dependencies like pystan.
	•	pandas + DBAPI Warnings: Harmless. They’re just suggestions for using SQLAlchemy.


Future Possibilities

	•	Real-Time Streaming: If you want live data, integrate Kafka or a similar tool.
	•	SKU-Level Detail: Expand from store-level to individual products.
	•	Cloud: If you ever want to scale up or show it publicly, consider GCP or AWS free tiers.


Author

Kokkanti Venkata Lohith
Master’s in Data Science & Applications, University at Buffalo


Thank you for checking out this local-first Digital Twin demo! It’s a great way to learn data engineering, transformations, forecasting, and simulation without racking up any cloud bills. If you have questions or feedback, feel free to reach out or file an issue. Happy tinkering!
