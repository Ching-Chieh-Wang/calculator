import os

class Config:

    # Database configuration (default to SQLite in project root)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "..", "history.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.abspath(DB_PATH)}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS configuration (allow Vue dev server on localhost:5173 by default)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    CORS_RESOURCES = {r"/api/*": {"origins": CORS_ORIGINS}}
