import pandas as pd
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2024, 1, 1)
days = 60
store_ids = [101, 102, 103]

# Generate store_operations.csv
store_data = []
for date in [start_date + timedelta(days=i) for i in range(days)]:
    for store_id in store_ids:
        sales = np.random.randint(100, 300)
        foot_traffic = sales + np.random.randint(20, 60)
        inventory = np.random.randint(400, 700)
        store_data.append([date.date(), store_id, sales, foot_traffic, inventory])

df_store = pd.DataFrame(store_data, columns=[
    'date', 'store_id', 'sales', 'foot_traffic', 'inventory_level'
])
df_store.to_csv('store_operations.csv', index=False)

# Generate supply_chain.csv
supply_data = []
for date in [start_date + timedelta(days=i) for i in range(days)]:
    for store_id in store_ids:
        arrivals = np.random.choice([0, 30, 50], p=[0.3, 0.4, 0.3])
        lead_time = np.random.randint(1, 5)
        reorder = np.random.randint(100, 250)
        supply_data.append([date.date(), store_id, arrivals, lead_time, reorder])

df_supply = pd.DataFrame(supply_data, columns=[
    'date', 'store_id', 'shipment_arrivals', 'lead_time_days', 'reorder_quantity'
])
df_supply.to_csv('supply_chain.csv', index=False)

print("✅ CSVs generated: store_operations.csv and supply_chain.csv")