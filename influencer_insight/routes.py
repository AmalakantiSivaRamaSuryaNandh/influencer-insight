"""HTTP routes for the web interface."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, render_template, request

from .services import (
    DataValidationError,
    available_categories,
    find_influencers,
    load_influencers,
    validate_category,
)


bp = Blueprint("main", __name__)


def _load_data():
    return load_influencers(current_app.config["DATA_PATH"])


@bp.get("/")
def home():
    return render_template("home.html")


@bp.route("/search", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def search():
    """Show the category form and return the highest-ranked match."""

    try:
        influencers = _load_data()
    except DataValidationError as exc:
        current_app.logger.exception("The influencer dataset is invalid")
        return render_template("search.html", categories=[], error=str(exc)), 500

    categories = available_categories(influencers)
    if request.method == "GET":
        return render_template("search.html", categories=categories)

    category, error = validate_category(request.form.get("category"), categories)
    if error:
        return (
            render_template(
                "search.html",
                categories=categories,
                error=error,
                selected_category=request.form.get("category", ""),
            ),
            400,
        )

    matches = find_influencers(influencers, category)
    if not matches:
        return (
            render_template(
                "search.html",
                categories=categories,
                error="No influencer matched that category. Try another category.",
                selected_category=category,
            ),
            404,
        )

    return render_template(
        "result.html",
        category=category,
        influencer=matches[0],
        alternatives=matches[1:3],
    )


@bp.get("/methodology")
def methodology():
    return render_template("methodology.html")


@bp.get("/health")
def health():
    """Small operational check added for local and hosted deployments."""

    try:
        count = len(_load_data())
    except DataValidationError as exc:
        return jsonify(status="error", message=str(exc)), 500
    return jsonify(status="ok", influencers=count)
