from typing import TypedDict, List, Dict

class OrderState(TypedDict):
    cust_id: str
    order_context: str
    query: str
    raw_agent_response: str
    final_response: str
    history: List[Dict[str, str]]
    intent: str
    evaluation: Dict[str, float]
    guard_result: str
    conv_guard_result: str
    evaluate_llm : any