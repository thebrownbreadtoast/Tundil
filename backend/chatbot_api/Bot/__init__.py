from flask import Blueprint
import json

module = Blueprint('bot',__name__)

@module.route('/', methods=['POST'])
def post():
    from backend.chatbot_api.Bot.views import Bot
    inference_response = Bot().bot_reply()
    reply = inference_response.get_data(as_text=True)
    del inference_response
    return reply

@module.route('/register', methods=['POST'])
def register():
    from backend.chatbot_api.Bot.views import Bot
    return Bot().register()