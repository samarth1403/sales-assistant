sql_forecasting_query_generator_examples = [
    {
        "question": "Total sales in SP-Hyd-Nexus Mall last month",
        "sql": """SELECT SUM(amount)
FROM sales_txn
JOIN o_site ON sales_txn.store_code = o_site.site_code
WHERE o_site.site_name = 'SP-Hyd-Nexus Mall'
  AND bill_time BETWEEN '2025-04-01 00:00:00' AND '2025-04-30 23:59:59';""",
    },
    {
        "question": "What is the number of transactions in Forum Nikita Mall in Q1 2025?",
        "sql": """SELECT COUNT(*)
FROM sales_txn
JOIN o_site ON sales_txn.store_code = o_site.site_code
WHERE o_site.site_name = 'Forum Nikita Mall'
  AND bill_time BETWEEN '2025-01-01 00:00:00' AND '2025-03-31 23:59:59';""",
    },
    {
        "question": "How many transactions happened in store code E099 on March 18, 2023?",
        "sql": """SELECT COUNT(*)
FROM sales_txn
WHERE store_code = 'E099'
  AND bill_time BETWEEN '2023-03-18 00:00:00' AND '2023-03-18 23:59:59';""",
    },
    {
        "question": "Average sales amount for store Forum Nikita Mall with store code E099 last year",
        "sql": """SELECT AVG(amount)
FROM sales_txn
JOIN o_site ON sales_txn.store_code = o_site.store_code
WHERE o_site.site_name = 'Forum Nikita Mall'
  AND o_site.site_code = 'E099'
  AND bill_time BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59';""",
    },
    {
        "question": "What will be sales for next 10 days from 31 march 2023 for 'E099' store",
        "sql": """
        SELECT
          sales_forecast.date,
          sales_forecast.predicted,
          sales_forecast.predicted_lower,
          sales_forecast.predicted_upper,
          sales_forecast.site_code,
          os.site_name
        FROM sales_forecast
        WHERE 
          sales_forecast.site_code = 'E099'
            join o_site os ON sales_forecast.site_code = o_site.site_code
          AND sales_forecast.is_deleted = 0
          AND sales_forecast.date BETWEEN '2023-04-01 00:00:00' AND '2023-04-10 23:59:59'
        ORDER BY
          sales_forecast.date ASC;""",
    },
]
