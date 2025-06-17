from langchain_core.prompts import PromptTemplate

comparative_query_result_prompt_prefix = PromptTemplate.from_template("""
    You are a data analyst. Given the results from two SQL queries representing the same metric over different time periods, write a concise and insightful summary.
    
    ### Metric:
    {metric}
    
    ### Time Periods:
    - Current Period: {time_period}
    - Baseline Period: {previous_time_period}
    
    ### Values:
    - Current Period Value: {current_value}
    - Baseline Period Value: {baseline_value}
    
    ### Goal:
    - Analyze the trend ({trend}) between the two periods.
    - Mention whether the metric has increased, decreased, or remained the same.
    - Include the percentage change in the output.
    - Use clear, business-friendly language (1–2 sentences).
    
    ### Output:
""")