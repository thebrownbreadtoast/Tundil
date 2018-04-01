from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.chatbot_api.Bot import module

class Server(object):

    def __init__(self):
        self.db = SQLAlchemy()

    def init_server(self,name=__name__):
        api = Flask(name)
        api.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dadwalakshay:itsaweakpassword@dadwalakshay.mysql.pythonanywhere-services.com/dadwalakshay$tundil'
        self.db.init_app(api)
        self.blueprints(api)
        return api

    def blueprints(self,api):
        api.register_blueprint(module,url_prefix='/bot')