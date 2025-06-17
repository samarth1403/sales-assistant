comparative_sql_query_generator_examples = [
  {
    "metric": "total sales amount",
    "trend": "increase",
    "time_period": "last month this year",
    "previous_time_period": "same month last year",
    "CURRENT_PERIOD_SQL": "SELECT SUM(amount) AS total_sales FROM sales_txn WHERE bill_time BETWEEN '2025-05-01 00:00:00' AND '2025-05-31 23:59:59';",
    "BASELINE_PERIOD_SQL": "SELECT SUM(amount) AS total_sales FROM sales_txn WHERE bill_time BETWEEN '2024-05-01 00:00:00' AND '2024-05-31 23:59:59';"
  },
  {
    "metric": "number of transactions",
    "trend": "decrease",
    "time_period": "this year",
    "previous_time_period": "last year",
    "CURRENT_PERIOD_SQL": "SELECT COUNT(*) AS transaction_count FROM sales_txn WHERE bill_time BETWEEN '2025-01-01 00:00:00' AND '2025-12-31 23:59:59';",
    "BASELINE_PERIOD_SQL": "SELECT COUNT(*) AS transaction_count FROM sales_txn WHERE bill_time BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59';"
  },
  {
    "metric": "average bill amount",
    "trend": "compare",
    "time_period": "Q1 of 2025",
    "previous_time_period": "Q2 of 2025",
    "CURRENT_PERIOD_SQL": "SELECT AVG(amount) AS avg_bill_amount FROM sales_txn WHERE bill_time BETWEEN '2025-04-01 00:00:00' AND '2025-06-30 23:59:59';",
    "BASELINE_PERIOD_SQL": "SELECT AVG(amount) AS avg_bill_amount FROM sales_txn WHERE bill_time BETWEEN '2025-01-01 00:00:00' AND '2025-03-31 23:59:59';"
  },
  {
    "metric": "total revenue",
    "trend": "compare",
    "time_period": "last 7 days",
    "previous_time_period": "previous 7 days",
    "CURRENT_PERIOD_SQL": "SELECT SUM(amount) AS total_revenue FROM sales_txn WHERE bill_time BETWEEN '2025-05-25 00:00:00' AND '2025-05-31 23:59:59';",
    "BASELINE_PERIOD_SQL": "SELECT SUM(amount) AS total_revenue FROM sales_txn WHERE bill_time BETWEEN '2025-05-18 00:00:00' AND '2025-05-24 23:59:59';"
  },
  {
    "metric": "unique bills",
    "trend": "compare",
    "time_period": "this week",
    "previous_time_period": "last week",
    "CURRENT_PERIOD_SQL": "SELECT COUNT(DISTINCT bill_no) AS unique_bills FROM sales_txn WHERE bill_time BETWEEN '2025-05-26 00:00:00' AND '2025-06-01 23:59:59';",
    "BASELINE_PERIOD_SQL": "SELECT COUNT(DISTINCT bill_no) AS unique_bills FROM sales_txn WHERE bill_time BETWEEN '2025-05-19 00:00:00' AND '2025-05-25 23:59:59';"
  }
]
