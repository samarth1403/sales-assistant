from langchain_core.prompts import PromptTemplate

query_classifier_prompt_prefix ="""
      You are an intelligent query classifier.

        Classify the following user input into one of these categories:
        - sql_query: if the user is asking for sales numbers, filters, or aggregations.
        - forecasting_query: if the user is asking about future sales or trends.
        - contextual_query: if the user wants analysis, insights, or reasoning.

        Input: {query}
        Category:                                              
"""
