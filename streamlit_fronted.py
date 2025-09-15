import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# Initialize session state
if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []
    # Loading the conversation history from the chatbot

# Display conversation history
for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# User input
user_input = st.chat_input("Type here")  

if user_input:
    # First add the message to the chat_history
    st.session_state['messages_history'].append({'role': 'user', 'content': user_input})

    with st.chat_message('user'):
        st.text(user_input)

    # Get chatbot response
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]})
    ai_message = response.content if hasattr(response, "content") else str(response)

    # Add assistant response to history
    st.session_state['messages_history'].append({'role': 'assistant', 'content': ai_message})

    with st.chat_message('assistant'):
        st.text(ai_message)
