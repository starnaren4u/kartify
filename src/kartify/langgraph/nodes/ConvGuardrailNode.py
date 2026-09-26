from langchain_core.messages import HumanMessage

from kartify.prompts.Prompts import CONVO_GUARDRAIL_PROMOPT
from kartify.model.OrderState import OrderState

def conversational_guard_node(state: OrderState):
    
    evaluate_llm = state["evaluate_llm"]
    convo_guard_prompt = CONVO_GUARDRAIL_PROMOPT.format(
        chat_history=state["history"]
        )

    state["conv_guard_result"] = evaluate_llm.invoke([HumanMessage(content=convo_guard_prompt)]).content.strip()
    return state

# ---- Guard Router ----
def conv_guard_router(state: OrderState):
    if state["conv_guard_result"] == "BLOCK":
        state["final_response"] = (
            "Your request is being forwarded to a customer support specialist."
        )
        return "exit_node"
    print("Assistant : "+state['final_response'])
    return "user_input"