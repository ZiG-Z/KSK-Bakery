from ksk import db , login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import app, current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    image_file = db.Column(db.String(30),nullable=False,default='default.png')

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def generate_token(self,expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expire_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def validate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        else:
            return User.query.get(user_id)


class Pizza(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product_code = db.Column(db.String,unique=True,nullable=False)
    type = db.Column(db.String,nullable=False)
    image_file = db.Column(db.String(30),nullable=False,default='default.jpg')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    product_detail = db.Column(db.Text,nullable=False)

    def __init__(self,product_code,type,product_detail,image_file='default.jpg'):
        self.product_code = product_code
        self.type = type
        self.product_detail = product_detail
        self.image_file = image_file
    

class BreadSnack(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product_code = db.Column(db.String,unique=True,nullable=False)
    type = db.Column(db.String,nullable=False)
    image_file = db.Column(db.String(30),nullable=False,default='default.jpg')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    product_detail = db.Column(db.Text,nullable=False)

    def __init__(self,product_code,type,product_detail,image_file='default.jpg'):
        self.product_code = product_code
        self.type = type
        self.product_detail = product_detail
        self.image_file = image_file

db.create_all()
