# from pyexpat import model
from sys import prefix
from typing import Dict, Any, cast
from src.utils.config import GOOGLE_API_KEY
from pydantic import SecretStr

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from .normal_response_formatter_prompt import normal_response_formatter_prompt

def get_normal_response_formatter_chain() -> Runnable[Dict[str, Any], str]:
    # GEMINI AI MODEL
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY must be a non-empty string.")

    llm_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", temperature=0, api_key=SecretStr(GOOGLE_API_KEY)
    )

    # 2. Define the Output Parser
    output_parser = StrOutputParser()

    # 3. Chaining together prompt and model using LCEL
    # The | operator chains runnables.
    # The `sql_query_generator_prompt` expects a dictionary with a 'text' key.
    # The `llm_model` takes the formatted prompt and returns an AI message.
    # The `output_parser` converts the AI message content to a sql query.
    normal_response_formatter_generator_chain = cast(
        Runnable[Dict[str, Any], str],
        normal_response_formatter_prompt | llm_model | output_parser,
    )

    return normal_response_formatter_generator_chain
