from flask import jsonify, request
from backend.chatbot_api.Bot.brain import Brain

class Bot(object):

    def bot_reply(self):
        try:
            header_key = Brain().user_validation(request.headers['apikey'])
        except:
            return jsonify({"reply":"API key not found"})
        else:
            if header_key:
                user_query = request.get_json()
                message = user_query['reply']
                return jsonify({"reply":Brain().tundil_bot(message)})
            else:
                return jsonify({"reply":"You are not Authorized to Access this Resource"})

    def register(self):
        user_data = request.get_json()
        name = user_data['name']
        phone = user_data['phone']
        return jsonify({"reply":str(Brain().user_register(name,phone))})

    def __del__(self):
        pass
