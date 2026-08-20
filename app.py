from flask import Flask
from views import views
from auth import auth
from models import db, User
from flask_login import LoginManager
from datetime import timedelta
from seed import fill_action

app = Flask(__name__)

app.config["SECRET_KEY"] = "aggawe4534"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

db.init_app(app)
with app.app_context():
    db.create_all()
    fill_action()

app.register_blueprint(views)
app.register_blueprint(auth)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)