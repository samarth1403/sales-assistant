# from pyexpat import model
from typing import Dict, Any, cast
from pydantic import SecretStr

from src.utils.config import GOOGLE_API_KEY

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from .comparative_query_result_prompt_prefix import comparative_query_result_prompt_prefix
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


def get_comparative_query_result_chain() -> Runnable[Dict[str, Any], str]:
    # OPEN AI MODEL
    # if not OPENAI_API_KEY:
    #     raise ValueError("OPENAI_API_KEY must be a non-empty string.")

    # 1. Create an LLM Model
    # llm_model = ChatOpenAI(
    #     model="gpt-3.5-turbo", temperature=0, api_key=SecretStr(OPENAI_API_KEY)
    # )

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
    # The `query_classifier_prompt` expects a dictionary with a 'text' key.
    # The `llm_model` takes the formatted prompt and returns an AI message.
    # The `output_parser` converts the AI message content to a string.
    comparative_query_result_chain = cast(
        Runnable[Dict[str, Any], str],
        comparative_query_result_prompt_prefix | llm_model | output_parser,
    )

    return comparative_query_result_chain
