from langchain_core.messages import HumanMessage

from kartify.model.OrderState import OrderState
from kartify.prompts.Prompts import INTENT_PROMPT


def intent_node(state: OrderState):

    evaluate_llm = state["evaluate_llm"]
    intent_prompt = INTENT_PROMPT.format(user_query=state["query"])
    print("intent_prompt")
    
    state["intent"] = evaluate_llm.invoke([HumanMessage(content=intent_prompt)]).content.strip()
    return state

# ---- Intent Router ----
def intent_router(state: OrderState):
    intent = state["intent"].strip()
    if intent == "2":
        return "order_agent"   # processable query → Agent
    else:
        return "exit_node"      # escalation / exit / out-of-scope