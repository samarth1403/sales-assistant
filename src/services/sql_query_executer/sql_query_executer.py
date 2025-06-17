import json
from src.db import get_raw_db
import psycopg2.extras
from src.services.response_formatter.generate_response import generate_response
from src.services.normal_response_formatter.generate_normal_response import generate_normal_response
from datetime import datetime

def sql_query_executer(sql_query, user_input):
    rdb = next(get_raw_db())
    cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    results = []
    try:
        print(f"Executing SQL query: {sql_query}")
        cursor.execute(sql_query.replace("```sql", "").replace("```", ""))
        results = cursor.fetchall()
        if not results:
            print("❗No data found for the given query.")
            return None
        else:
            # Getting Error in this generate_response function ( Need to check later )
            # return generate_response(user_input, len(results) == 1 and results[0] or results)
            for item in results:
                if 'date' in item and isinstance(item['date'], datetime):
                    item['date'] = item['date'].isoformat()  # Or use strftime for custom formatting
            return generate_normal_response(user_input, json.dumps(results))
    except Exception as e:
        print(f"❗Error executing SQL query: {e}")
        return None
        # print(generate_normal_response(user_input, json.dumps(results))) # Written this
        # to handle all edge cases and return a normal response
