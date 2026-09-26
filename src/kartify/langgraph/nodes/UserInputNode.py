from kartify.model.OrderState import OrderState

def user_input_node(state: OrderState):
    if not (state.get("cust_id") or "").strip():
        while True:
            customer_id = input("Please enter your Customer ID: ").strip()
            if customer_id:
                state["cust_id"] = customer_id
                break
            print("Customer ID cannot be blank.")

    user_query = input("How can I help you? ")
    state["query"] = user_query
    return state
