from langchain_core.prompts import PromptTemplate

normal_response_formatter_prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant that summarizes raw SQL query results in a friendly, concise, and informative tone.
    
    User Question:
    {question}
    
    SQL Result:
    {result}
    The SQL Result is in JSON format.
    Please summarize it naturally.
    The price is indian rupees.
    Generate a clear and natural response to the user based on this result.
    """
)