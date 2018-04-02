from backend.chatbot_api import Server

db = Server().db

class User(db.Model):

    def __init__(self,apikey,name,phone):
        self.apikey = apikey
        self.name = name
        self.phone = phone

    __tablename__ = 'user'
    apikey = db.Column(db.String(10))
    name = db.Column(db.String(20))
    phone = db.Column(db.BIGINT,primary_key=True)