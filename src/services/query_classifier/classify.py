from .query_classifier_chain import get_query_classifier_chain


def classify_query(user_query: str) -> str:
    query_query_classifier_chain = get_query_classifier_chain()
    response = query_query_classifier_chain.invoke({"query": user_query})
    return response.strip().lower()
