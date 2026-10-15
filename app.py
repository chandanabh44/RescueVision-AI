"""
RescueVision AI - Main Application Entrypoint
AI-Powered Disaster Detection, Early Warning and Emergency Response System
"""

import os
import logging
from flask import Flask, send_from_directory, render_template, jsonify
from config import Config
from models import db
from routes import main_bp, incident_bp, ai_bp, admin_bp, api_bp
from services.external_data_service import ExternalDataService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("rescuevision")


def create_app(config_class=Config):
    """Application factory for RescueVision AI."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(incident_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Secure file serving for verified user-uploaded imagery
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if app.request_class.is_json:
            return jsonify({"status": "error", "message": "Resource not found"}), 404
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "status": "error",
            "message": "File exceeds maximum upload limit (10MB). Please choose a smaller image."
        }), 413

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        if app.request_class.is_json:
            return jsonify({"status": "error", "message": "Internal server error"}), 500
        return render_template("500.html"), 500

    # Auto-initialize database tables and initial data sources safely
    with app.app_context():
        db.create_all()
        try:
            ExternalDataService.init_sources()
        except Exception as e:
            logger.warning(f"Could not auto-initialize data sources: {e}")

    return app


# WSGI application instance for production deployment (Waitress / Gunicorn)
app = create_app()


if __name__ == "__main__":
    logger.info("Starting RescueVision AI Server...")
    logger.info(f"Access local dashboard at: http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
