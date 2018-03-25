from flask import Blueprint

module = Blueprint('bot',__name__)

@module.route('/', methods=['GET'])
def post():
    from backend.chatbot_api.chat.views import bot
    return bot().chat_bot_response()