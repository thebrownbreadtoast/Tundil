from flask import Blueprint

module = Blueprint('employees',__name__)

@module.route('/', methods=['GET'])
def post():
    from chatbot_api.chat.views import bot
    return bot().chat_bot_response()