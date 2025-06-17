from .followup_handler_chain import get_followup_handler_chain

def get_followup_question(context: str, question: str) -> str:
    followup_handler_chain = get_followup_handler_chain()
    response = followup_handler_chain.invoke({"context": context, "question": question})
    return response.strip()