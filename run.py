from backend.chatbot_api import chat_init

if __name__ == '__main__':
    app = chat_init().server(__name__)
    app.run(host='0.0.0.0',debug=True,port=7464)