from backend.chatbot_api import Server

if __name__ == '__main__':
	api = Server().init_server(__name__)
	api.run(port=7464)
