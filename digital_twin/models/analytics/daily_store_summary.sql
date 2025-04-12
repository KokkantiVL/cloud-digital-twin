SELECT
  so.date,
  so.store_id,
  so.sales,
  so.foot_traffic,
  so.inventory_level,
  sc.shipment_arrivals,
  sc.lead_time_days,
  sc.reorder_quantity
FROM {{ ref('stg_store_operations') }} so
LEFT JOIN {{ ref('stg_supply_chain') }} sc
  ON so.date = sc.date
  AND so.store_id = sc.store_id