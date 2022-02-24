from flask import Flask
from flask_mail import Mail
from .config import Config
print("INIT CALLED")
print(Config.SECRET_KEY)

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
from app import views 
