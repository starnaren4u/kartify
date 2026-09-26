from kartify.agent.OrderAgent import order_agent
from kartify.model.OrderState import OrderState

def order_agent_node(state: OrderState):
    order_context, final_response = order_agent(
        query=state['query'],
        history=state['history']
    )
    state["order_context"] = order_context
    state["final_response"] = final_response
    
    return state