from .other_questions_chain import get_other_questions_chain


def get_other_questions_answer(user_query: str) -> str:
    other_questions_chain = get_other_questions_chain()
    response = other_questions_chain.invoke({"question": user_query})
    return response.strip()
