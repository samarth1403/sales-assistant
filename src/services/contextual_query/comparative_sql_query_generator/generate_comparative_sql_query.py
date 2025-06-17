import json
import re
import json
from src.db import get_raw_db
import psycopg2.extras
from src.services.response_formatter.generate_response import generate_response
from src.services.normal_response_formatter.generate_normal_response import generate_normal_response
from datetime import datetime
from .comparative_sql_query_generator_chain import get_comparative_sql_query_generator_chain
from src.services.contextual_query.comparative_query_result.get_comparative_query_result import get_comparative_query_result


def generate_comparative_sql_query(metric: str, trend: str, time_period: str, previous_time_period: str) -> str:
    response = get_comparative_sql_query_generator_chain()
    sql_query = response.invoke({"metric": metric, "trend": trend, "time_period": time_period, "previous_time_period": previous_time_period})

    pattern = r"(\w+):\n```sql\n(.*?)\n```"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    # Convert to dictionary
    sql_dict = {key: sql.strip() for key, sql in matches}

    current_period_results = sql_query_executer(sql_dict.get('CURRENT_PERIOD_SQL'))
    baseline_period_results = sql_query_executer(sql_dict.get('BASELINE_PERIOD_SQL'))

    for item in current_period_results:
        if 'date' in item and isinstance(item['date'], datetime):
            item['date'] = item['date'].isoformat()

    for item in baseline_period_results:
        if 'date' in item and isinstance(item['date'], datetime):
            item['date'] = item['date'].isoformat()

    return get_comparative_query_result(metric, trend, time_period, previous_time_period,
                                         json.dumps(current_period_results),
                                         json.dumps(baseline_period_results)
                                        )

def sql_query_executer(sql_query):
    rdb = next(get_raw_db())
    cursor = rdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    results = []
    try:
        print(f"Executing SQL query: {sql_query}")
        cursor.execute(sql_query)
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
            return results
    except Exception as e:
        print(f"❗Error executing SQL query: {e}")
        return None
        # print(generate_normal_response(user_input, json.dumps(results))) # Written this
        # to handle all edge cases and return a normal response
