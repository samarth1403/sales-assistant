params_extraction_examples = [
  {
    "query": "Why did sales drop last week?",
    "response": '{{ "metric": "sales", "trend": "drop", "time_period": "last week", "previous_time_period": "the week before last" }}'
  },
  {
    "query": "Why did sales rise last month?",
    "response": '{{ "metric": "sales", "trend": "rise", "time_period": "last month", "previous_time_period": "the month before last" }}'
  },
  {
    "query": "What caused the spike in transactions yesterday?",
    "response": '{{ "metric": "transactions", "trend": "spike", "time_period": "yesterday", "previous_time_period": "day before yesterday" }}'
  },
  {
    "query": "Why were there fewer transactions in May?",
    "response": '{{ "metric": "transactions", "trend": "decrease", "time_period": "May", "previous_time_period": "April" }}'
  },
  {
    "query": "Why did revenue rise this quarter?",
    "response": '{{ "metric": "revenue", "trend": "rise", "time_period": "this quarter", "previous_time_period": "last quarter" }}'
  },
  {
    "query": "Why did sales rise on Black Friday?",
    "response": '{{ "metric": "sales", "trend": "rise", "time_period": "Black Friday", "previous_time_period": "the same weekday of the previous week" }}'
  },
  {
    "query": "Why did orders decrease during the holiday season?",
    "response": '{{ "metric": "orders", "trend": "decrease", "time_period": "the holiday season", "previous_time_period": "same season last year" }}'
  }
]