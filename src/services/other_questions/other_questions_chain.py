# from pyexpat import model
from typing import Dict, Any, cast
from pydantic import SecretStr

from src.utils.config import GOOGLE_API_KEY
from .other_questions_prompt_prefix import other_questions_prompt_prefix
from .other_questions_examples import other_questions_examples

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


def get_other_questions_chain() -> Runnable[Dict[str, Any], str]:
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
        "Question: {question}\nResponse: {response}\n"
    )

    query_classifier_few_shot_prompt = FewShotPromptTemplate(
        examples=other_questions_examples,
        example_prompt=query_classifier_example_prompt,
        input_variables=["question"],
        prefix=other_questions_prompt_prefix,
        suffix="Question: {question}\nResponse:",
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
