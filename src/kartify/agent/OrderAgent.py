from datetime import date

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from kartify.langgraph.nodes.ConvGuardrailNode import conv_guard_router, conversational_guard_node
from kartify.langgraph.nodes.DebugNode import debug_node
from kartify.langgraph.nodes.EvaluationNode import evaluation_node, retry_router
from kartify.langgraph.nodes.ExitNode import exit_node
from kartify.langgraph.nodes.GuardRailNode import guard_node, guard_router
from kartify.langgraph.nodes.IntentNode import intent_node, intent_router
from kartify.langgraph.nodes.MemoryNode import memory_node
from kartify.langgraph.nodes.UserInputNode import user_input_node
from kartify.model.ConversationMemory import conversation_memory
from kartify.model.OrderState import OrderState
from kartify.prompts.Prompts import SYSTEM_PROMPT
from kartify.tools.OrderDetails import fetch_order_details


def run_chatbot():
    from kartify.langgraph.nodes.OrderAgentNode import order_agent_node

    conversation_memory.clear()

    graph = StateGraph(OrderState)
    
    graph.add_node("user_input",       debug_node("user_input",       user_input_node))
    graph.add_node("intent_classifier",debug_node("intent",           intent_node))
    graph.add_node("order_agent",      debug_node("order_agent",      order_agent_node))
    graph.add_node("evaluate",         debug_node("evaluate",         evaluation_node))
    graph.add_node("safety_check",     debug_node("safety_check",     guard_node))
    graph.add_node("conv_safety_check",debug_node("conv_safety_check",conversational_guard_node))
    graph.add_node("memory_save",      debug_node("memory_save",      memory_node))
    graph.add_node("exit_node",        debug_node("exit_node",        exit_node))
    
    graph.set_entry_point("user_input")
    graph.add_edge("user_input",  "intent_classifier")
    graph.add_conditional_edges(
        "intent_classifier", intent_router,
        {"order_agent": "order_agent", "exit_node": "exit_node"}
    )
    graph.add_edge("order_agent", "evaluate")
    graph.add_conditional_edges(
        "evaluate", retry_router,
        {"order_agent": "order_agent", "safety_check": "safety_check"}
    )
    graph.add_conditional_edges(
        "safety_check", guard_router,
        {"memory_save": "memory_save", "exit_node": "exit_node"}
    )
    graph.add_edge("memory_save", "conv_safety_check")
    graph.add_conditional_edges(
        "conv_safety_check", conv_guard_router,
        {"user_input": "user_input", "exit_node": "exit_node"}
    )
    graph.add_edge("exit_node", END)

    order_graph = graph.compile()
    
    initial_state: OrderState = {
        "cust_id": "",
        "order_context": "",
        "query": "",
        "raw_agent_response": "",
        "final_response": "",
        "history": conversation_memory.get(),
        "intent": "",
        "evaluation": {},
        "guard_result": "",
        "conv_guard_result": "",
        "evaluate_llm" : ChatOpenAI(model_name="gpt-4o-mini")
    }
    config = {"recursion_limit": 100}
    order_graph.invoke(initial_state, config=config)


def order_agent(query: str, history: list) -> tuple[str, str]:
    """
    Order Agent — combines policy reasoning and answer generation.
    Returns (order_context, final_response).
    """
    # We are using a fixed date as our data is static and this date best resembles with the database

    # Initialise the LLM — used by Policy Agent, Answer Agent (tool-calling), and guardrails
    llm = ChatOpenAI(model_name="gpt-4o-mini")
    
    # Bind the SQL tool to the LLM
    llm_with_tools = llm.bind_tools([fetch_order_details])

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

        print("Messages : ", messages)

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
