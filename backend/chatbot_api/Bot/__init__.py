from flask import Blueprint
import json, gc

module = Blueprint('bot',__name__)

@module.route('/', methods=['POST'])
def post():
    from backend.chatbot_api.Bot.views import Bot
    inference_response = Bot().bot_reply()
    return inference_response

@module.route('/register', methods=['POST'])
def register():
    from backend.chatbot_api.Bot.views import Bot
    return Bot().register()