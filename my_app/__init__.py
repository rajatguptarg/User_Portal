from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
#engine = create_engine('postgresql://postgres:postgres@localhost/user_info')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rajat:rajat@localhost/user_info'
db = SQLAlchemy(app)


from my_app.portal.views import portal
app.register_blueprint(portal)


db.create_all()