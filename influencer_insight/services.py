"""Dataset validation, NLP preprocessing, and influencer ranking."""

from __future__ import annotations

import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


REQUIRED_COLUMNS = {
    "username",
    "display_name",
    "bio",
    "category",
    "followers",
    "likes",
    "comments",
    "shares",
}
METRIC_COLUMNS = ("followers", "likes", "comments", "shares")
CATEGORY_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s-]*$")

# Used only when the optional NLTK stopwords corpus has not been downloaded.
FALLBACK_STOPWORDS = frozenset(
    "a an and are as at be by for from has have in into is it of on or that the "
    "their this to was were will with your you our we".split()
)

_LEMMATIZER = WordNetLemmatizer()
_STEMMER = PorterStemmer()


class DataValidationError(ValueError):
    """Raised when the CSV cannot be used safely by the application."""


@lru_cache(maxsize=1)
def _english_stopwords() -> frozenset[str]:
    try:
        return frozenset(stopwords.words("english"))
    except LookupError:
        return FALLBACK_STOPWORDS


@lru_cache(maxsize=4096)
def _normalise_token(token: str) -> str:
    """Lemmatize a token, with an offline NLTK stemmer fallback."""

    try:
        noun_form = _LEMMATIZER.lemmatize(token, pos="n")
        return _LEMMATIZER.lemmatize(noun_form, pos="v")
    except LookupError:
        # PorterStemmer is part of NLTK and requires no downloaded corpus.
        return _STEMMER.stem(token)


def preprocess_text(text: object) -> str:
    """Lowercase, tokenize, remove stopwords, and normalize English text."""

    if text is None:
        return ""

    tokens = wordpunct_tokenize(str(text).lower())
    cleaned = []
    for token in tokens:
        if not token.isalnum() or token in _english_stopwords():
            continue
        cleaned.append(_normalise_token(token))
    return " ".join(cleaned)


def _non_negative_number(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a number") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be a non-negative finite number")
    return number


def calculate_influence_score(
    followers: object,
    likes: object,
    comments: object,
    shares: object,
) -> float:
    """Return the report-inspired weighted influence score.

    The source report names the four metrics but does not publish exact weights.
    These transparent implementation weights are therefore an explicit assumption.
    """

    values = {
        "followers": _non_negative_number(followers, "followers"),
        "likes": _non_negative_number(likes, "likes"),
        "comments": _non_negative_number(comments, "comments"),
        "shares": _non_negative_number(shares, "shares"),
    }
    return round(
        values["followers"] * 0.10
        + values["likes"] * 0.40
        + values["comments"] * 0.30
        + values["shares"] * 0.20,
        2,
    )


def calculate_engagement_rate(
    followers: object,
    likes: object,
    comments: object,
    shares: object,
) -> float:
    """Return engagement as a percentage of followers."""

    follower_count = _non_negative_number(followers, "followers")
    interactions = sum(
        _non_negative_number(value, label)
        for label, value in (
            ("likes", likes),
            ("comments", comments),
            ("shares", shares),
        )
    )
    if follower_count == 0:
        return 0.0
    return round((interactions / follower_count) * 100, 2)


def load_influencers(csv_path: str | Path) -> list[dict]:
    """Read and validate the influencer CSV, then add derived metrics."""

    path = Path(csv_path)
    if not path.is_file():
        raise DataValidationError(f"Dataset not found: {path}")

    try:
        frame = pd.read_csv(path)
    except (OSError, pd.errors.ParserError) as exc:
        raise DataValidationError("The influencer dataset could not be read.") from exc

    missing = sorted(REQUIRED_COLUMNS.difference(frame.columns))
    if missing:
        raise DataValidationError(
            "Dataset is missing required columns: " + ", ".join(missing)
        )
    if frame.empty:
        raise DataValidationError("The influencer dataset is empty.")

    for column in ("username", "display_name", "bio", "category"):
        if frame[column].isna().any() or (frame[column].astype(str).str.strip() == "").any():
            raise DataValidationError(f"Dataset column '{column}' contains empty values.")
        frame[column] = frame[column].astype(str).str.strip()

    for column in METRIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
        if frame[column].isna().any() or (frame[column] < 0).any():
            raise DataValidationError(
                f"Dataset column '{column}' must contain non-negative numbers."
            )
        frame[column] = frame[column].astype(int)

    records = frame[list(REQUIRED_COLUMNS)].to_dict(orient="records")
    for record in records:
        record["category"] = record["category"].lower()
        record["influence_score"] = calculate_influence_score(
            record["followers"],
            record["likes"],
            record["comments"],
            record["shares"],
        )
        record["engagement_rate"] = calculate_engagement_rate(
            record["followers"],
            record["likes"],
            record["comments"],
            record["shares"],
        )
    return records


def available_categories(influencers: Iterable[dict]) -> list[str]:
    return sorted({str(item["category"]).strip().lower() for item in influencers})


def validate_category(
    raw_category: object, categories: Iterable[str]
) -> tuple[str | None, str | None]:
    """Normalize and validate a category submitted by the form."""

    category = " ".join(str(raw_category or "").strip().lower().split())
    if not category:
        return None, "Please choose an influencer category."
    if len(category) > 40:
        return None, "Category must be 40 characters or fewer."
    if not CATEGORY_PATTERN.fullmatch(category):
        return None, "Category may contain only letters, spaces, and hyphens."

    allowed = {str(item).strip().lower() for item in categories}
    if category not in allowed:
        return None, "Please choose one of the available categories."
    return category, None


def find_influencers(influencers: Iterable[dict], category: str) -> list[dict]:
    """Find NLP token matches and return them in score order."""

    query_tokens = set(preprocess_text(category).split())
    if not query_tokens:
        return []

    matches = []
    for influencer in influencers:
        searchable_text = f"{influencer['category']} {influencer['bio']}"
        candidate_tokens = set(preprocess_text(searchable_text).split())
        if query_tokens.issubset(candidate_tokens):
            matches.append(influencer)

    return sorted(
        matches,
        key=lambda item: (item["influence_score"], item["followers"]),
        reverse=True,
    )
