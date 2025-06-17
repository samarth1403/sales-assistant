from .response_formatter_chain import get_response_formatter_chain

def generate_response(question: str, result) -> str:
    response_formatter_chain = get_response_formatter_chain()
    response = response_formatter_chain.invoke({"question": question, "result": result})
    return response.strip() if response else "No response generated."