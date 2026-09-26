from langchain_core.messages import HumanMessage

from kartify.prompts.Prompts import GUARDRAIL_PROMOPT
from kartify.model.OrderState import OrderState


def guard_node(state: OrderState):

    evaluate_llm = state["evaluate_llm"]

    guardrail_prompt = GUARDRAIL_PROMOPT.format(
        final_response = state["final_response"]
    )

    state["guard_result"] = evaluate_llm.invoke([HumanMessage(content=guardrail_prompt)]).content.strip()
    return state

# ---- Guard Router ----
def guard_router(state: OrderState):
    if state["guard_result"] == "BLOCK":
        state["final_response"] = (
            "Your request is being forwarded to a customer support specialist."
        )
        return "exit_node"
    return "memory_save"