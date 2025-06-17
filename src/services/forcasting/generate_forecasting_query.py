from .sql_forecasting_query_generator_chain import (
    get_sql_forecasting_query_generator_chain,
)

def generate_forecasting_sql_query(user_query: str) -> str:
    response = get_sql_forecasting_query_generator_chain()
    sql_forecasting_query = response.invoke({"question": user_query})
    return sql_forecasting_query.strip()
