from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()

def init_extensions(app):
    cors.init_app(app, resources=app.config["CORS_RESOURCES"])
    db.init_app(app)