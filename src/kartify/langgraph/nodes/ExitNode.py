from kartify.model.OrderState import OrderState

def exit_node(state: OrderState):
    if state["intent"] == "0":
        state["final_response"] = "Sorry for the inconvenience. A human support agent will assist you shortly."
    elif state["intent"] == "1":
        state["final_response"] = "Thank you! I hope I was able to assist with your query."
    elif state["intent"] == "3":
        state["final_response"] = "Apologies, I’m currently only able to help with information about your placed orders."

    print("Assistant :"+state['final_response'])
    return state