from .sql_query_generator_chain import get_sql_query_generator_chain


def generate_sql_query(user_query: str) -> str:
    response = get_sql_query_generator_chain()
    sql_query = response.invoke({"question": user_query})
    return sql_query.strip()
