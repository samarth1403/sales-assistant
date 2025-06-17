# from pyexpat import model
from typing import Dict, Any, cast
from pydantic import SecretStr

from src.utils.config import GOOGLE_API_KEY
from .query_classifier_prompt_prefix import query_classifier_prompt_prefix
from .query_classifier_examples import query_classifier_examples

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


def get_query_classifier_chain() -> Runnable[Dict[str, Any], str]:
    """
    Creates and returns an LLM chain for query classification using LCEL ( Langchain expression language).

    The chain expects a dictionary with a 'text' key as input and
    returns a string (the predicted category).

    Returns:
        Runnable[Dict[str, Any], str]: An LCEL chain for query classification.
    """
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

    query_classifier_example_prompt = PromptTemplate.from_template(
        "Query: {query}\nCategory: {category}\n"
    )

    query_classifier_few_shot_prompt = FewShotPromptTemplate(
        examples=query_classifier_examples,
        example_prompt=query_classifier_example_prompt,
        input_variables=["query"],
        prefix=query_classifier_prompt_prefix,
        suffix="Query: {query}\nCategory:",
    )

    # 2. Define the Output Parser
    output_parser = StrOutputParser()

    # 3. Chaining together prompt and model using LCEL
    # The | operator chains runnables.
    # The `query_classifier_prompt` expects a dictionary with a 'text' key.
    # The `llm_model` takes the formatted prompt and returns an AI message.
    # The `output_parser` converts the AI message content to a string.
    query_classifier_chain = cast(
        Runnable[Dict[str, Any], str],
        query_classifier_few_shot_prompt | llm_model | output_parser,
    )

    return query_classifier_chain
