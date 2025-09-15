from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.messages import add_messages
from langgraph.checkpoint.memory import InMemoryCheckpointSaver

# Load environment variables (expects GROQ_API_KEY in .env)
load_dotenv()

# Initialize LLM
llm = ChatGroq(model="gemma2-9b-it")

# Define the state schema
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Define a node that sends messages to the LLM
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Use an in-memory checkpoint (conversation history)
checkpointer = InMemoryCheckpointSaver()

# Build the graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile chatbot
chatbot = graph.compile(checkpointer=checkpointer)
