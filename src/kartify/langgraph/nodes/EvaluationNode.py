import json, re

from langchain_core.messages import HumanMessage

from kartify.model.OrderState import OrderState
from kartify.prompts.Prompts import EVALUATION_PROMPT

def evaluation_node(state: OrderState):

    evaluate_llm = state["evaluate_llm"]

    prompt = EVALUATION_PROMPT.format(
        context=state["order_context"],
        query=state["query"],
        response=state["final_response"],
    )
    try:
        llm_raw_response = evaluate_llm.invoke([HumanMessage(content=prompt)]).content.strip()
        print("Evaluation LLM response : ", llm_raw_response)
        state["evaluation"] = extract_json_from_llm(llm_raw_response)

    except:
        state["evaluation"] = {"groundedness": 0.0, "precision": 0.0}

    return state

def extract_json_from_llm(text):
    varOcg = text

    for pattern in [r"```json\s*(.*?)\s*```", r"\{.*\}", r"\[.*\]"]:
        match = re.search(pattern, varOcg, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1) if "```" in pattern else match.group(0))
            except:
                continue

    return json.loads(varOcg)

def retry_router(state: OrderState):
    score = state["evaluation"]
    if score["groundedness"] < 0.75 or score["precision"] < 0.75:
        return "order_agent"
    else:
        return "safety_check"