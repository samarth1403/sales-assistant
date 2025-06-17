params_extraction_prompt_prefix = """
    You are a smart assistant that extracts structured information from user queries about sales or business performance.
    
    Your task is to extract the following fields from the user's query {query}:
    
    1. metric: What is the topic or metric of interest? (e.g., sales, returns, signups)
    2. trend: What kind of change or event occurred? (e.g., increase, decrease, drop, spike, rise, fall)
    3. time_period: What is the main time period being referred to? (e.g., yesterday, last week, May 2025)
    4. previous_time_period: What is the comparison or baseline time period mentioned (if any)? (e.g., previous week, April 2025)
    
    Return your output in the following JSON format:
    
    {{
      "metric": "...",
      "trend": "...",
      "time_period": "...",
      "previous_time_period": "..."
    }}
"""
