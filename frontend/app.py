import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.chat_engine import ChatEngine
from datetime import datetime
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatEngine()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "chats" not in st.session_state:
    st.session_state.chats = {}

st.set_page_config(page_title="AI Mental Health Chatbot", page_icon="🧠", layout="wide")
with st.sidebar:
    st.title("💬 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True, key="new_chat"):
        st.session_state.current_chat_id = None
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    if st.session_state.chats:
        st.subheader("Recent Chats")
        for chat_id, chat_info in sorted(
            st.session_state.chats.items(), 
            key=lambda x: x[1]["timestamp"], 
            reverse=True
        ):
            title = chat_info["title"][:30]
            
            col1, col2 = st.columns([0.85, 0.15])
            
            with col1:
                if st.button(
                    title,
                    use_container_width=True,
                    key=f"chat_{chat_id}",
                ):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.messages = chat_info["messages"]
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    del st.session_state.chats[chat_id]
                    if st.session_state.current_chat_id == chat_id:
                        st.session_state.current_chat_id = None
                        st.session_state.messages = []
                    st.rerun()
    else:
        st.info("No chats yet. Start a new conversation!")
    
    st.divider()
    st.caption("Your conversations are private")

st.title("Mental Health Support Chatbot")
st.write("Get emotional support, coping strategies, and AI-powered recommendations.")

st.divider()

chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info("Start a new conversation or select one from the sidebar.")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

st.divider()

if prompt := st.chat_input("Share what you're feeling..."):
    if st.session_state.current_chat_id is None:
        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.current_chat_id = chat_id
        st.session_state.chats[chat_id] = {
            "title": prompt[:50],
            "timestamp": datetime.now(),
            "messages": []
        }
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your emotions..."):
            response_obj = st.session_state.chatbot.get_response(prompt)
            
            if hasattr(response_obj, "content"):
                response_text = response_obj.content
            else:
                response_text = str(response_obj)
        
        st.markdown(response_text)
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
    
    st.rerun()