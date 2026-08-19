# Influencer Insight

[![Tests](https://github.com/AmalakantiSivaRamaSuryaNandh/influencer-insight/actions/workflows/tests.yml/badge.svg)](https://github.com/AmalakantiSivaRamaSuryaNandh/influencer-insight/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-6c43e0.svg)](LICENSE)

**Live application:** [https://influencer-insight.onrender.com](https://influencer-insight.onrender.com)

Repository reconstructed and maintained by
[Amalakanti Siva Rama Surya Nandh](https://github.com/AmalakantiSivaRamaSuryaNandh).

**Influencer Insight: Unveiling Top Instagram Influencers Using NLP** is a
complete, Git-ready reconstruction of the Flask application described in the
final-year project report. A user selects an influencer category, NLTK processes
the sample biographies, and a transparent engagement formula ranks the matching
profiles.

> Educational scope: all names, usernames, biographies, and metrics in the CSV
> are fictional sample data. The project does not connect to Instagram or claim
> to measure real people.

## Project information

| Field | Details |
|---|---|
| Project title | **Influencer Insight: Unveiling Top Instagram Influencers Using Natural Language Processing (NLP)** |
| Programme | **B.Tech – CSE (Artificial Intelligence & Data Science)** |
| Institution | **Kakinada Institute of Engineering & Technology** |
| Academic period | **2020–2024** |
| Project guide | **Ms. Bavirisetti Himagiri Nandini, M.Tech, Assistant Professor** |
| Project type | Five-member final-year group project |
| Domain | Natural language processing, data analysis, influencer ranking |
| Demonstrated stack | Python, Flask, Pandas, NLTK, HTML and CSS |
| Repository data | 24 fictional sample profiles in a local CSV file |

## Original academic project team

| Student | Roll number |
|---|---|
| Amalakanti Siva Rama Surya Nandh | 20B21A45C7 |
| Nukala Sai Sri Pavan | 20B21A45C9 |
| Bainapalli Balu | 20B21A45D6 |
| Nurukurthi Bhuvana Shankar | 21B25A4515 |
| Ills Satya Sekar | 21B25A4518 |

The table uses the spellings on the project report's cover page. The
presentation and report contain a few conflicting names and feature claims;
these are recorded transparently in the
[document consistency audit](docs/document-audit.md).

## Project story

The original five-member team completed this topic as part of the B.Tech CSE –
Artificial Intelligence and Data Science programme. Amalakanti Siva Rama Surya
Nandh later rebuilt the demonstrated idea as a complete, maintainable Flask
application to refresh the concepts, understand every part of the
implementation, and share a runnable version with other learners.

The source report describes a simple CSV + NLTK + weighted-ranking application.
It does not provide every source file, template, dataset field, or exact score
weight. This repository therefore separates the report-inspired behavior from
the engineering additions made during the reconstruction. The assumptions are
documented in the methodology page, tests, and the "Additions beyond the
original document" section below.

## What the application does

1. Loads and validates influencer records from a CSV file with Pandas.
2. Accepts a category such as fashion, food, travel, or technology.
3. Uses NLTK to lowercase, tokenize, remove stop words, and lemmatize text.
4. Matches the selected category to normalized category and biography tokens.
5. Scores followers, likes, comments, and shares with visible weights.
6. Shows the top profile and two alternative matches in a responsive interface.

The core flow is intentionally simple because that is what the implementation
section of the source report describes. No trained machine-learning model or
Instagram API credentials are required.

For a claim-by-claim comparison of the report, presentation, and working
repository, see [`docs/document-audit.md`](docs/document-audit.md).

## Technology

- Python 3.10 or newer
- Flask
- Pandas
- NLTK
- HTML and CSS
- pytest and pytest-cov for automated tests

## Quick start

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install the application

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Optional but recommended: download the NLTK corpora used for the full stop-word
list and WordNet lemmatization.

```bash
python scripts/download_nltk_data.py
```

The application still runs without those downloads. In offline environments it
uses a small built-in stop-word list and NLTK's corpus-free Porter stemmer.

### 3. Run the application

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

For Flask's development reload mode:

```powershell
$env:FLASK_DEBUG = "1"
python app.py
```

Do not use the development server as a public production server. `wsgi.py`
provides a WSGI entry point for a production server when you are ready to host
the app.

## Run the tests

Install the development tools and execute the suite:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Optional coverage report:

```bash
python -m pytest --cov=influencer_insight --cov-report=term-missing
```

## Scoring method and assumption

The report says followers, likes, comments, and shares are assigned different
weights, but it does **not** state the exact formula. This implementation makes
the assumption explicit and testable:

```text
influence score =
    followers × 0.10
  + likes       × 0.40
  + comments    × 0.30
  + shares      × 0.20
```

The score selects the top match. The interface also shows this contextual metric:

```text
engagement rate = (likes + comments + shares) / followers × 100
```

You can change the weights in
`influencer_insight/services.py::calculate_influence_score`, then update the
related service test and the methodology page so the behavior remains clear.

## Input validation

- The category is required, limited to 40 characters, and accepts only letters,
  spaces, and hyphens.
- Only categories that exist in the validated dataset are accepted.
- CSV text cells cannot be empty.
- Metric fields must be non-negative numbers.
- Missing or malformed data produces a clear error instead of an unsafe ranking.

## Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Introduction page |
| `/search` | GET, POST | Category form and ranked result |
| `/index` | GET, POST | Compatibility alias for the route named in the report |
| `/methodology` | GET | NLP and scoring explanation |
| `/health` | GET | Small JSON application/data check |

## Project structure

```text
influencer-insight/
├── app.py                         # Local development entry point
├── wsgi.py                        # Production WSGI entry point
├── docs/
│   └── document-audit.md          # PDF-to-repository consistency review
├── influencer_insight/
│   ├── __init__.py                # Flask application factory
│   ├── routes.py                  # Web routes and validation flow
│   ├── services.py                # CSV, NLP, and scoring logic
│   ├── static/css/style.css       # Responsive visual design
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── search.html
│       ├── result.html
│       ├── methodology.html
│       └── 404.html
├── data/
│   ├── influencers.csv            # 24 fictional sample profiles
│   └── README.md                  # Dataset schema and usage note
├── scripts/
│   └── download_nltk_data.py      # Optional NLTK corpus setup
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   └── test_services.py
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

Repository support files also include `AUTHORS.md`, `CITATION.cff`,
`SECURITY.md`, `CODE_OF_CONDUCT.md`, `render.yaml`, `.python-version`, and the
GitHub workflow, issue-template, pull-request-template, and Dependabot files
under `.github/`.

## Additions beyond the original document

The following are recommended engineering improvements, clearly separated from
the report's described implementation:

| Addition | Why it was added |
|---|---|
| Application factory and service modules | Keeps routes, analysis, and configuration testable and easier to explain |
| CSV schema and numeric validation | Prevents silent or misleading rankings from malformed data |
| Offline NLTK fallback | Keeps the demo usable before optional corpora are downloaded |
| Engagement-rate display | Adds context without changing the report-inspired ranking |
| Alternative matches | Makes the result more useful while retaining one clear top result |
| `/health` endpoint and `wsgi.py` | Makes future hosting and status checks easier |
| Responsive, keyboard-friendly UI and 404 page | Improves usability and accessibility |
| Automated pytest suite | Verifies NLP, scoring, validation, routes, and error behavior |
| Git files, license, contribution guide, and dataset note | Makes the repository safer and easier to publish |
| GitHub Actions and Dependabot | Runs tests for pushes and pull requests and proposes dependency updates |
| Citation, authorship, security, and conduct files | Makes ownership and community expectations explicit |
| Render deployment configuration | Provides a production WSGI deployment path instead of Flask's development server |

## Known limitations and responsible use

- This is a learning demonstration using a static, fictional dataset.
- The score is a manually chosen heuristic, not a validated business KPI.
- Bio keyword matching is NLP preprocessing, not a trained classifier.
- Real influencer discovery would require authorized, policy-compliant data,
  data freshness checks, fraud detection, audience-quality analysis, privacy
  review, and bias evaluation.
- Never scrape or publish personal data without permission and a lawful basis.

## Customize the dataset

Edit `data/influencers.csv` while preserving these columns:

```text
username, display_name, bio, category, followers, likes, comments, shares
```

Keep metrics as non-negative whole numbers. Run `python -m pytest` after a data
change; several tests also verify the included sample rows and total count, so
update those expectations when intentionally replacing the sample data.

## Deployment

The application is deployed at
[influencer-insight.onrender.com](https://influencer-insight.onrender.com).
This repository includes `render.yaml`, `wsgi.py`, Gunicorn, and a fixed Python
version for reproducible Render deployment. Changes to `main` are tested by
GitHub Actions before the hosted service is updated.

## Attribution

The original academic work belongs to the five-member team listed above. This
repository reconstruction is maintained by **Amalakanti Siva Rama Surya
Nandh** ([GitHub](https://github.com/AmalakantiSivaRamaSuryaNandh)).

For complete attribution, see [`AUTHORS.md`](AUTHORS.md). Citation metadata for
both the software reconstruction and original academic project is available in
[`CITATION.cff`](CITATION.cff).

## License

Released under the MIT License. See `LICENSE`.
