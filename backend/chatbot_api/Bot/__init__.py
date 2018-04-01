from flask import Blueprint

module = Blueprint('bot',__name__)

@module.route('/', methods=['POST'])
def post():
    from backend.chatbot_api.Bot.views import Bot
    return Bot().bot_reply()

@module.route('/register', methods=['POST'])
def register():
    from backend.chatbot_api.Bot.views import Bot
    return Bot().register()