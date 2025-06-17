from .params_extraction_chain import (
    get_params_extraction_chain,
)

def get_extracted_params(user_query: str) -> str:
    response = get_params_extraction_chain()
    params = response.invoke({"query": user_query})
    return params
