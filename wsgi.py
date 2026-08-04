"""WSGI entry point for production servers."""

from influencer_insight import create_app


app = create_app()
