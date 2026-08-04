from pathlib import Path

import pytest

from influencer_insight.services import (
    DataValidationError,
    available_categories,
    calculate_engagement_rate,
    calculate_influence_score,
    find_influencers,
    load_influencers,
    preprocess_text,
    validate_category,
)


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "influencers.csv"


def test_preprocess_text_lowercases_tokenizes_and_removes_stopwords():
    processed = preprocess_text("The TECHNOLOGY creators, with useful tools!")

    tokens = processed.split()
    assert "the" not in tokens
    assert "with" not in tokens
    assert "technolog" in tokens or "technology" in tokens
    assert all(token.isalnum() for token in tokens)


def test_influence_score_uses_documented_implementation_weights():
    score = calculate_influence_score(1000, 100, 20, 10)

    assert score == 148.0


def test_score_rejects_negative_input():
    with pytest.raises(ValueError, match="non-negative"):
        calculate_influence_score(-1, 100, 20, 10)


def test_engagement_rate_handles_zero_followers():
    assert calculate_engagement_rate(0, 100, 20, 10) == 0.0


def test_dataset_loads_and_exposes_categories():
    influencers = load_influencers(DATA_PATH)

    assert len(influencers) == 24
    assert available_categories(influencers) == [
        "beauty",
        "fashion",
        "fitness",
        "food",
        "technology",
        "travel",
    ]
    assert all("influence_score" in item for item in influencers)


def test_technology_profiles_are_sorted_by_score():
    influencers = load_influencers(DATA_PATH)
    matches = find_influencers(influencers, "technology")

    assert len(matches) == 4
    assert matches[0]["username"] == "bytewithneha"
    assert matches[0]["influence_score"] >= matches[1]["influence_score"]


def test_no_nlp_match_returns_empty_list():
    influencers = load_influencers(DATA_PATH)

    assert find_influencers(influencers, "astronomy") == []


def test_category_validation_accepts_normalized_known_value():
    result, error = validate_category("  TECHNOLOGY ", ["technology", "travel"])

    assert result == "technology"
    assert error is None


def test_missing_csv_columns_raise_clear_error(tmp_path):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("username,bio\nuser,hello\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="missing required columns"):
        load_influencers(invalid_csv)
