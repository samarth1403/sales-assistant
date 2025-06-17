response_formatter_examples = [
    {
        "question": "What was the total sales in March 2024?",
        "result": {'sum': 48520},
        "response": "The total sales in March 2024 amounted to ₹48,520."
    },
    {
        "question": "How many transactions happened in store E099 on May 12?",
        "result": [{"count": 312}],
        "response": "There were 312 transactions in store E099 on May 12."
    },
    {
        "question": "Average bill value in Forum Sujana Mall for February 2025?",
        "result": [{"avg": 654.32}],
        "response": "The average bill value in Forum Sujana Mall for February 2025 was ₹654.32."
    },
    {
        "question": "List total sales per month in Q1 2024",
        "result": [{"month": "January", "total": 30500}, {"month": "February", "total": 29800}, {"month": "March", "total": 32000}],
        "response": (
            "Here’s the total sales per month in Q1 2024:\n"
            "- January: ₹30,500\n"
            "- February: ₹29,800\n"
            "- March: ₹32,000"
        )
    },
    {
        "question": "Give me the number of transactions per store for June 2024.",
        "result": [{"store_code": "E101", "count": 220}, {"store_code": "E102", "count": 310}, {"store_code": "E103", "count": 185}],
        "response": (
            "Here are the number of transactions per store for June 2024:\n"
            "- Store E101: 220 transactions\n"
            "- Store E102: 310 transactions\n"
            "- Store E103: 185 transactions"
        )
    },
]
