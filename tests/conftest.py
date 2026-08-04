from pathlib import Path

import pytest

from influencer_insight import create_app


@pytest.fixture()
def app():
    project_root = Path(__file__).resolve().parents[1]
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "DATA_PATH": str(project_root / "data" / "influencers.csv"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()
