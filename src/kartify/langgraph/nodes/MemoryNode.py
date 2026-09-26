from kartify.model.ConversationMemory import conversation_memory
from kartify.model.OrderState import OrderState

def memory_node(state: OrderState):
    conversation_memory.add(
         {"user": state["query"], "assistant": state["final_response"]}
        )
    return state
