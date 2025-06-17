# from pyexpat import model
from sys import prefix
from typing import Dict, Any, cast
from src.utils.config import GOOGLE_API_KEY
from pydantic import SecretStr

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from src.services.followup_handler.followup_handler_examples import followup_handler_examples
from src.services.followup_handler.followup_handler_prompt_prefix import followup_handler_prompt_prefix

def get_followup_handler_chain() -> Runnable[Dict[str, Any], str]:
    # GEMINI AI MODEL
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY must be a non-empty string.")

    llm_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", temperature=0, api_key=SecretStr(GOOGLE_API_KEY)
    )

    followup_handler_chain_example_prompt = PromptTemplate.from_template(
          "Conversation History:\n{context}\n\nFollow-up Question:\n{question}\n\nRewritten Standalone Question:\n{reformulated}\n---\n"
    )

    followup_handler_chain_few_shot_prompt = FewShotPromptTemplate(
        examples = followup_handler_examples,
        example_prompt=followup_handler_chain_example_prompt,
        input_variables=["context", "question"],
        prefix=followup_handler_prompt_prefix,
        suffix="Conversation History:\n{context}\n\nFollow-up Question:\n{question}\n\nRewritten Standalone Question:",
    )

    # 2. Define the Output Parser
    output_parser = StrOutputParser()

    # 3. Chaining together prompt and model using LCEL
    # The | operator chains runnables.
    # The `sql_query_generator_prompt` expects a dictionary with a 'text' key.
    # The `llm_model` takes the formatted prompt and returns an AI message.
    # The `output_parser` converts the AI message content to a sql query.
    followup_handler_chain = cast(
        Runnable[Dict[str, Any], str],
        followup_handler_chain_few_shot_prompt | llm_model | output_parser,
    )

    return followup_handler_chain
