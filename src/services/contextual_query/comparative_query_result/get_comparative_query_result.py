from .comparative_query_result_chain import get_comparative_query_result_chain

def get_comparative_query_result(metric: str, trend: str, time_period: str, previous_time_period: str,
                                 current_value: str, baseline_value: str) -> str:
    response = get_comparative_query_result_chain()
    answer = response.invoke({
        'metric': metric,
        'trend': trend,
        'time_period': time_period,
        'previous_time_period': previous_time_period,
        'current_value': current_value,
        'baseline_value': baseline_value,
    })
    return answer.strip()
