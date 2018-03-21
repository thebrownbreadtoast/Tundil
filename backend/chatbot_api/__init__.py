from flask import Flask
from chatbot_api.chat import module

class chat_init(object):

    def __init__(self):
        pass

    def server(self,name=__name__):
        app = Flask(name)
        self.blueprints(app)
        return app

    def blueprints(self,app):
        app.register_blueprint(module,url_prefix='/bot')