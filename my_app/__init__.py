from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os


DFAULT_DB_URI = "postgresql://rgupta1@docker.for.mac.host.internal/user_info"
DB_URI = os.getenv('DB_URI', DFAULT_DB_URI)


app = Flask(__name__)
#engine = create_engine('postgresql://postgres:postgres@localhost/user_info')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)


from my_app.portal.views import portal
app.register_blueprint(portal)


db.create_all()
