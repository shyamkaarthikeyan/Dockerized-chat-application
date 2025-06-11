import streamlit as st
import socketio
import asyncio
import threading
import time
import json
import os
from datetime import datetime
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="Real-time Chat with LLM",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .llm-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .system-message {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .message-header {
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .message-content {
        font-size: 1rem;
    }
    .message-time {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.3rem;
    }
    .typing-indicator {
        font-style: italic;
        color: #666;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .stButton > button {
        width: 100%;
    }
    .online-users {
        background-color: #e8f5e8;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'online_users' not in st.session_state:
    st.session_state.online_users = []
if 'llm_typing' not in st.session_state:
    st.session_state.llm_typing = False
if 'socket' not in st.session_state:
    st.session_state.socket = None

# Socket.IO client setup
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3001')

class SocketManager:
    def __init__(self):
        self.sio = socketio.Client()
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.sio.event
        def connect():
            st.session_state.connected = True
            
        @self.sio.event
        def disconnect():
            st.session_state.connected = False
            
        @self.sio.event
        def user_info(data):
            st.session_state.user_info = data
            
        @self.sio.event
        def message(data):
            st.session_state.messages.append(data)
            
        @self.sio.event
        def chat_history(data):
            st.session_state.messages = data
            
        @self.sio.event
        def users_update(data):
            st.session_state.online_users = data
            
        @self.sio.event
        def user_joined(data):
            system_msg = {
                'id': f"system_{int(time.time())}",
                'username': '📢 System',
                'content': f"{data['username']} joined the chat",
                'timestamp': data['timestamp'],
                'type': 'system'
            }
            st.session_state.messages.append(system_msg)
            
        @self.sio.event
        def user_left(data):
            system_msg = {
                'id': f"system_{int(time.time())}",
                'username': '📢 System',
                'content': f"{data['username']} left the chat",
                'timestamp': data['timestamp'],
                'type': 'system'
            }
            st.session_state.messages.append(system_msg)
            
        @self.sio.event
        def llm_typing(data):
            st.session_state.llm_typing = data.get('isTyping', False)
    
    def connect_to_server(self, username):
        try:
            self.sio.connect(BACKEND_URL)
            self.sio.emit('join', {'username': username})
            return True
        except Exception as e:
            st.error(f"Failed to connect to server: {str(e)}")
            return False
    
    def send_message(self, content):
        if self.sio.connected:
            self.sio.emit('message', {'content': content})
    
    def send_llm_message(self, content, model):
        if self.sio.connected:
            self.sio.emit('llm_message', {'content': content, 'model': model})
    
    def disconnect_from_server(self):
        if self.sio.connected:
            self.sio.disconnect()

# Initialize socket manager
if 'socket_manager' not in st.session_state:
    st.session_state.socket_manager = SocketManager()

# Main UI
st.title("💬 Real-time Chat with LLM")
st.markdown("Powered by Ollama, Socket.IO, and Streamlit")

# Sidebar for connection and settings
with st.sidebar:
    st.header("Connection")
    
    if not st.session_state.connected:
        username = st.text_input("Enter your username:", value="", placeholder="Your name...")
        
        available_models = ["llama3.2", "mistral", "codellama", "neural-chat"]
        selected_model = st.selectbox("Select LLM Model:", available_models)
        
        if st.button("Connect to Chat"):
            if username.strip():
                st.session_state.username = username.strip()
                if st.session_state.socket_manager.connect_to_server(username.strip()):
                    st.session_state.selected_model = selected_model
                    st.rerun()
            else:
                st.error("Please enter a username")
    else:
        st.success(f"✅ Connected as: {st.session_state.username}")
        
        if st.session_state.user_info:
            st.info(f"User ID: {st.session_state.user_info.get('id', 'N/A')}")
        
        # Online users
        st.subheader("Online Users")
        if st.session_state.online_users:
            for user in st.session_state.online_users:
                st.write(f"👤 {user['username']}")
        else:
            st.write("No users online")
        
        # Model selection
        available_models = ["llama3.2", "mistral", "codellama", "neural-chat"]
        st.session_state.selected_model = st.selectbox(
            "LLM Model:", 
            available_models, 
            index=available_models.index(st.session_state.get('selected_model', 'llama3.2'))
        )
        
        if st.button("Disconnect"):
            st.session_state.socket_manager.disconnect_from_server()
            st.session_state.connected = False
            st.session_state.messages = []
            st.session_state.online_users = []
            st.rerun()

# Main chat area
if st.session_state.connected:
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        st.subheader("Chat Messages")
        
        # Display messages
        for message in st.session_state.messages:
            msg_type = message.get('type', 'user')
            username = message.get('username', 'Unknown')
            content = message.get('content', '')
            timestamp = message.get('timestamp', '')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S')
            except:
                time_str = timestamp
            
            # Choose message style based on type
            if msg_type == 'user':
                css_class = "user-message"
            elif msg_type == 'llm':
                css_class = "llm-message"
            elif msg_type == 'system':
                css_class = "system-message"
            else:
                css_class = "error-message"
            
            st.markdown(f"""
            <div class="chat-message {css_class}">
                <div class="message-header">{username}</div>
                <div class="message-content">{content}</div>
                <div class="message-time">{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Typing indicator
        if st.session_state.llm_typing:
            st.markdown("""
            <div class="typing-indicator">
                🤖 LLM is typing...
            </div>
            """, unsafe_allow_html=True)
    
    # Message input area
    st.subheader("Send Message")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        message_input = st.text_area(
            "Type your message:", 
            value="", 
            height=100,
            placeholder="Enter your message here..."
        )
    
    with col2:
        st.write("Send Options:")
        
        if st.button("💬 Send to Chat"):
            if message_input.strip():
                st.session_state.socket_manager.send_message(message_input.strip())
                st.rerun()
        
        if st.button("🤖 Ask LLM"):
            if message_input.strip():
                st.session_state.socket_manager.send_llm_message(
                    message_input.strip(), 
                    st.session_state.selected_model
                )
                st.rerun()
    
    # Auto-refresh to show new messages
    if st.button("🔄 Refresh"):
        st.rerun()
    
    # Auto-refresh every 2 seconds
    time.sleep(2)
    st.rerun()

else:
    st.info("👈 Please connect to the chat using the sidebar")
    
    # Show connection status
    st.subheader("Server Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend server is running")
        else:
            st.error("❌ Backend server is not responding properly")
    except:
        st.error("❌ Cannot connect to backend server")
    
    st.markdown("""
    ### How to use:
    1. Enter your username in the sidebar
    2. Select an LLM model
    3. Click "Connect to Chat"
    4. Start chatting with other users
    5. Use "Ask LLM" to get responses from the AI model
    
    ### Features:
    - Real-time messaging with Socket.IO
    - Multiple user support
    - Local LLM integration via Ollama
    - User presence indicators
    - Chat history
    - Multiple LLM models support
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Socket.IO, and Ollama")