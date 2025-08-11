from flask import Flask, jsonify
from config.config import Config
from extensions import init_extensions
from controllers.calculate_controller import bp as calc_bp
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    init_extensions(app)

    # create tables (simple app — no migrations)
    with app.app_context():
        db.create_all()

    # blueprints
    app.register_blueprint(calc_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"])