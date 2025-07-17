import operator
import os
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from tools import buy_sweet, get_available_sweets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. Define Tools and Agent State ---
tools = [buy_sweet, get_available_sweets]


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# --- 2. Define Graph Nodes ---
from langchain_core.messages import SystemMessage

# System prompt to set context about currency and business
SYSTEM_PROMPT = """You are a helpful assistant for a sweet shop. Here are important details about your business:

1. **Currency**: All prices in the database are in Indian Rupees (INR). Always display prices with ₹ symbol or mention "INR".
2. **Role**: You help customers browse available sweets and process purchases.
3. **Tools**: You have access to:
   - get_available_sweets: To check current inventory
   - buy_sweet: To process purchases
4. **Behavior**: Be friendly, helpful, and always confirm purchase details before processing.

Always call get_available_sweets first to show available sweets and rely on that data, dont depend on data available in previous message history.

For purchased, in success message, always say user that purchase is successful, you can check dashboard that quantity is decreased. Because i am showing this app to someone, to whom i want that he/she notice that after purchase, quantity is decreased in dashboard.

Only give answer in plain text, no HTML or Markdown formatting.

When showing prices, always use the ₹ symbol (e.g., ₹15.99) or mention "INR" to be clear about the currency."""

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)


def call_model(state: AgentState):
    """The node that calls the LLM to decide on the next action."""
    messages = state["messages"]

    # Add system prompt if it's not already the first message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# --- 3. Define the Graph's Conditional Logic ---
def should_continue(state: AgentState):
    """If the LLM made a tool call, run the tool. Otherwise, end."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "call_tool"
    return "end"


# --- 4. Wire up the Simplified Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"call_tool": "tools", "end": END},
)
workflow.add_edge("tools", "agent")

graph = workflow.compile()


# --- 5. Add History to the Graph ---
def get_agent_with_history(session_id: str, redis_url: Optional[str] = None):
    """
    Create an agent with chat history using Redis.
    Returns a function that can be called with user messages.
    """
    # Use provided redis_url or get from environment
    if redis_url is None:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    def chat_with_history(user_message: str):
        # Get chat history
        history = RedisChatMessageHistory(session_id, url=redis_url)

        # Prepare the state with history + new message
        # Get existing messages from history
        existing_messages = history.messages

        # Add the new user message
        new_message = HumanMessage(content=user_message)
        all_messages = existing_messages + [new_message]

        # Create state
        state = AgentState(messages=all_messages)

        # Run the graph
        result = graph.invoke(state)

        # Get the final response
        final_message = result["messages"][-1]

        # Save the conversation to history
        history.add_message(new_message)
        history.add_message(final_message)

        return final_message

    return chat_with_history


# --- 6. Graph Visualization ---
def generate_graph_diagram(output_path: str = "agent_graph.png"):
    """
    Generates a visual diagram of the LangGraph workflow and saves it as a PNG file.

    Args:
        output_path (str): Path where the PNG file will be saved. Defaults to "agent_graph.png"

    Returns:
        str: Success message with the file path or error message
    """
    try:
        # Generate the graph visualization
        graph_image = graph.get_graph().draw_mermaid_png()

        # Save the image to file
        with open(output_path, "wb") as f:
            f.write(graph_image)

        return f"Graph diagram successfully saved to: {output_path}"

    except Exception as e:
        return f"Error generating graph diagram: {str(e)}"


# Generate the graph diagram when the module is imported (optional)
if __name__ == "__main__":
    result = generate_graph_diagram()
    print(result)
