from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail



app = Flask(__name__)

app.config['SECRET_KEY'] = 'b4ea539a892923b3e1771ade579ee0fa'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ksk.db"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 456
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'zigz5638@gmail.com'
app.config['MAIL_PASSWORD'] = "FUCK YOU"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
    
from ksk.main.routes import main
from ksk.users.routes import users
from ksk.pizza.routes import pizzas
from ksk.breaksnack.routes import breadsnacks
from ksk.cake.routes import cakes

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(pizzas)
app.register_blueprint(breadsnacks)
app.register_blueprint(cakes)


