from flask import jsonify, request

class bot(object):

    def chat_bot_response(self):
        return jsonify({"reply":"This is a response from Bot."})


# class security(object):

#     def register(self):
#         meta_data = request.get_json()
#         name = meta_data['name']
#         keygen = api.security().apiregister(name)
#         return jsonify("Hey, "+keygen+" your API key has been Generated, Please contact Authority.")