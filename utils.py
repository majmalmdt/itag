from flask_bcrypt import Bcrypt
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import MetaData
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cpses_ied6p7g0hm@localhost/devoskil_enterprise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'manvabaksksvsjukvkap'
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
bcrypt = Bcrypt(app)
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
CORS(app)

ALLOWED_IMAGE_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.svg'])

IMAGE_FOLDER = './static/images/'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
