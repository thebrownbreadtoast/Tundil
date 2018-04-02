from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.chatbot_api.Bot import module
import pymysql

class Server(object):

    def __init__(self):
        self.db = SQLAlchemy()

    def init_server(self,name=__name__):
        api = Flask(name)
        pymysql.install_as_MySQLdb()
        api.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/dadwalakshay'
        self.db.init_app(api)
        self.blueprints(api)
        return api

    def blueprints(self,api):
        api.register_blueprint(module,url_prefix='/bot')