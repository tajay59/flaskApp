from flask import Flask
from flask_mail import Mail
from .config import Config 
from .models import UserProfile 
from flask_login import LoginManager
print(Config.SECRET_KEY)

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views 
