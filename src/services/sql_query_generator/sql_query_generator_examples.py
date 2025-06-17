sql_query_generator_examples = [
    {
        "question": "Show the forecasted sales for Forum Sujana Mall in the next 7 days",
        "sql": """SELECT sales_forecast.date, sales_forecast.predicted, sales_forecast.predicted_lower, sales_forecast.predicted_upper
FROM sales_forecast
JOIN o_site ON sales_forecast.site_code = o_site.site_code
WHERE o_site.site_name = 'Forum Sujana Mall'
  AND o_site.is_deleted = 0
  AND o_site.is_active = 1
  AND sales_forecast.is_deleted = 0
  AND sales_forecast.date BETWEEN '2025-05-28 00:00:00' AND '2025-06-03 23:59:59'
ORDER BY sales_forecast.date ASC;""",
    },
    {
        "question": "Forecast for store code E099 for the next month",
        "sql": """SELECT sales_forecast.date, sales_forecast.predicted, sales_forecast.predicted_lower, sales_forecast.predicted_upper
FROM sales_forecast
WHERE sales_forecast.site_code = 'E099'
  AND sales_forecast.is_deleted = 0
  AND sales_forecast.date BETWEEN '2025-06-01 00:00:00' AND '2025-06-30 23:59:59'
ORDER BY sales_forecast.date ASC;""",
    },
    {
        "question": "Predicted sales in SU-Hyd-Nexus Mall in Q3 2025",
        "sql": """SELECT sales_forecast.date, sales_forecast.predicted, sales_forecast.predicted_lower, sales_forecast.predicted_upper
FROM sales_forecast
JOIN o_site ON sales_forecast.site_code = o_site.site_code
WHERE o_site.site_name = 'SU-Hyd-Nexus Mall'
  AND o_site.is_deleted = 0
  AND o_site.is_active = 1
  AND sales_forecast.is_deleted = 0
  AND sales_forecast.date BETWEEN '2025-07-01 00:00:00' AND '2025-09-30 23:59:59'
ORDER BY sales_forecast.date ASC;""",
    },
    {
        "question": "Forecasted sales for E099 for December 2025",
        "sql": """SELECT sales_forecast.date, sales_forecast.predicted, sales_forecast.predicted_lower, sales_forecast.predicted_upper
FROM sales_forecast
WHERE sales_forecast.site_code = 'E099'
  AND sales_forecast.is_deleted = 0
  AND sales_forecast.date BETWEEN '2025-12-01 00:00:00' AND '2025-12-31 23:59:59'
ORDER BY sales_forecast.date ASC;""",
    },
    {
        "question": "Forecasted sales for Forum Sujana Mall for this year",
        "sql": """SELECT sales_forecast.date, sales_forecast.predicted, sales_forecast.predicted_lower, sales_forecast.predicted_upper
FROM sales_forecast
JOIN o_site ON sales_forecast.site_code = o_site.site_code
WHERE o_site.site_name = 'Forum Sujana Mall'
  AND o_site.is_deleted = 0
  AND o_site.is_active = 1
  AND sales_forecast.is_deleted = 0
  AND sales_forecast.date BETWEEN '2025-01-01 00:00:00' AND '2025-12-31 23:59:59'
ORDER BY sales_forecast.date ASC;""",
    },
]
