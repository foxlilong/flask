from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)




from app import routes, model, forms

print(app.url_map)

# db.drop_all()
# db.create_all()
# us1 = model.User(username='john1', email='john1@example.com')
# us2 = model.User(username='john2', email='john2@example.com')
# db.session.add_all([us1, us2])
# db.session.commit()
