from datetime import date

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from kartify.model.OrderState import OrderState
from kartify.prompts.Prompts import SYSTEM_PROMPT
from kartify.tools.OrderDetails import fetch_order_details

def order_agent_node(state: OrderState):
    order_context, final_response = order_agent(
        state,
        query=state['query'],
        history=state['history'],
    )
    state["order_context"] = order_context
    state["final_response"] = final_response
    
    return state

def order_agent(state: OrderState, query: str, history: list) -> tuple[str, str]:
    """
    Order Agent — combines policy reasoning and answer generation.
    Returns (order_context, final_response).
    """
    # We are using a fixed date as our data is static and this date best resembles with the database

    # Initialise the LLM — used by Policy Agent, Answer Agent (tool-calling), and guardrails
    agent_llm = state["agent_llm"]
    
    # Bind the SQL tool to the LLM
    llm_with_tools = agent_llm.bind_tools([fetch_order_details])

    today = date.today().strftime("%d %b").lstrip("0")

    # Build conversation history text
    history_text = ""
    if history:
        history_text = "\nPrevious conversation:\n" + "\n".join(
            f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history
        ) + "\n"

    user_content = f"Previous Coversation:{history_text}\n Customer query: {query}\nToday's date: {today}"

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content)
    ]

    order_context = ""
    max_iterations = 5  # safety cap on the loop

    for _ in range(max_iterations):
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        # If no tool calls → the agent produced its Final Answer
        if not getattr(ai_msg, 'tool_calls', None):
            break

        # Execute each tool call (Observation step)
        for tc in ai_msg.tool_calls:
            if tc['name'] == 'fetch_order_details':
                result = fetch_order_details.invoke(tc['args'])
                order_context = result  # save for evaluation
                messages.append(ToolMessage(content=result, tool_call_id=tc['id']))

    final_response = ai_msg.content.strip()

    # Strip any residual prefixes if the model left them in
    for prefix in ("Final Answer:", "final answer:"):
        if final_response.lower().startswith(prefix.lower()):
            final_response = final_response[len(prefix):].strip()
            break

    return order_context, final_response