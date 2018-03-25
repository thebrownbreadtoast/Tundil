from backend.chatbot_api import chat_init
app = chat_init().server(__name__)
