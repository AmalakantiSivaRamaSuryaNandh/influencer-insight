"""Application factory for the Influencer Insight Flask app."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, render_template


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure an application instance."""

    app = Flask(__name__)
    project_root = Path(__file__).resolve().parent.parent

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "local-development-key"),
        DATA_PATH=str(project_root / "data" / "influencers.csv"),
        MAX_CONTENT_LENGTH=16 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    from .routes import bp

    app.register_blueprint(bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app
