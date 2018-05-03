from backend.chatbot_api import Server
# api = Server().init_server(__name__)

if __name__ == '__main__':
	api = Server().init_server(__name__)
	api.run('0.0.0.0')
