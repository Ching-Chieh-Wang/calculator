from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy

cors = CORS()
db = SQLAlchemy()

def init_extensions(app):
    cors.init_app(app, resources={r"/*": {"origins": app.config["CORS_ORIGIN"]}})
    db.init_app(app)