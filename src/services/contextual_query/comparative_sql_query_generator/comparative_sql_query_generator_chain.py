# from pyexpat import model
from typing import Dict, Any, cast
from src.utils.config import GOOGLE_API_KEY
from pydantic import SecretStr
from .comparative_sql_query_generator_prompt_prefix import (
    comparative_sql_query_generator_prompt_prefix,
)
from .comparative_sql_query_generator_examples import (
    comparative_sql_query_generator_examples,
)

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate


def get_comparative_sql_query_generator_chain() -> Runnable[Dict[str, Any], str]:
    # GEMINI AI MODEL
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY must be a non-empty string.")

    llm_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", temperature=0, api_key=SecretStr(GOOGLE_API_KEY)
    )

    comparative_sql_query_generator_example_prompt = PromptTemplate.from_template("""
        Metric: {metric}\n
        Trend: {trend}\n
        Time Period: {time_period}\n
        Previous Time Period: {previous_time_period}\n
        CURRENT_PERIOD_SQL:
        {CURRENT_PERIOD_SQL}\n
        BASELINE_PERIOD_SQL:
        {BASELINE_PERIOD_SQL}\n
        """
    )

    comparative_sql_generator_few_shot_prompt = FewShotPromptTemplate(
        examples=comparative_sql_query_generator_examples,
        example_prompt=comparative_sql_query_generator_example_prompt,
        input_variables=["metric", "trend", "time_period", "previous_time_period"],
        prefix=comparative_sql_query_generator_prompt_prefix,
        suffix="""
            Metric: {metric}
            Trend: {trend}
            Time Period: {time_period}
            Previous Time Period: {previous_time_period}
            CURRENT_PERIOD_SQL:
            BASELINE_PERIOD_SQL:
        """
    )

    # 2. Define the Output Parser
    output_parser = StrOutputParser()

    # 3. Chaining together prompt and model using LCEL
    # The | operator chains runnables.
    # The `sql_query_generator_prompt` expects a dictionary with a 'text' key.
    # The `llm_model` takes the formatted prompt and returns an AI message.
    # The `output_parser` converts the AI message content to a sql query.
    comparative_sql_query_generator_chain = cast(
        Runnable[Dict[str, Any], str],
        comparative_sql_generator_few_shot_prompt | llm_model | output_parser,
    )

    return comparative_sql_query_generator_chain
