# Project document consistency audit

This review compares the B.Tech final-year presentation, the 55-page project
report, and the working code in this repository. The source PDFs are academic
references; their statements are not treated as proof that a feature exists.
Only behavior visible in the implementation or supported by evidence is listed
as implemented.

## Source documents reviewed

- `ASRSN_B-Tech Final Year project ppt.pdf` (26 pages)
- `ASRSN_Final Year Project Document.pdf` (55 pages)

The PDFs are not included in this repository because they contain academic and
personal information.

## Verified project identity

| Item | Canonical repository value | Evidence and decision |
|---|---|---|
| Formal title | Influencer Insight: Unveiling Top Instagram Influencers Using Natural Language Processing (NLP) | Uses the full report-cover title |
| Programme | B.Tech – CSE (Artificial Intelligence & Data Science) | Report cover |
| Institution | Kakinada Institute of Engineering & Technology | Report cover and certificate |
| Academic period | 2020–2024 | Report cover |
| Guide | Ms. Bavirisetti Himagiri Nandini, M.Tech | Report cover, certificate, declaration, and presentation page 2 |
| Project type | Five-member final-year group project | Report cover, certificate, and declaration |

## Document identity corrections

These differences should be corrected in the academic files before they are
used as a final or official submission:

1. Presentation page 1 names **Mr. T. Manikanta, M.Tech** as the guide, while
   presentation page 2 and the report repeatedly name **Ms. B. Himagiri
   Nandini, M.Tech**. The report's bonafide certificate provides the full name
   **Ms. Bavirisetti Himagiri Nandini**; this repository uses that value.
2. The fifth team member appears as **Ills Satya Sekar**, **Ills Satya Sekhar**,
   and **Illa Satya Sekar** in different places. This repository uses **Ills
   Satya Sekar**, the report-cover spelling, with roll number 21B25A4518.
3. The presentation adds **Teja** to Nukala Sai Sri Pavan's name, while the
   report cover, certificate, declaration, and roll-number list omit it. This
   repository follows the report value: **Nukala Sai Sri Pavan**.
4. The title alternates between shortened forms and the full “Using Natural
   Language Processing (NLP)” form. The full report-cover title should be used
   consistently.

The college's official student and guide records remain the final authority if
any spelling must be changed.

## Claim-by-claim implementation check

| Document claim | Repository status | Finding |
|---|---|---|
| Python and Flask web application | Implemented | Application factory, routes, templates, and production entry point are present |
| CSV-based influencer dataset | Implemented with a safe substitute | The repository contains 24 explicitly fictional profiles |
| Pandas data loading | Implemented | The CSV schema and numeric fields are validated before use |
| NLTK text normalization | Implemented | Lowercasing, tokenization, stop-word removal, and lemmatization are used, with an offline fallback |
| Category-based matching | Implemented | Category and biography tokens are matched deterministically |
| Weighted followers, likes, comments, and shares | Implemented with a documented assumption | The report names the metrics but does not provide exact weights; the repository exposes its chosen weights |
| Return a top influencer | Implemented | The highest-scoring match is shown with two supporting alternatives |
| HTML and CSS interface | Implemented | Responsive Flask templates and styling are included |
| Real-time Instagram API integration | Not implemented | There are no Instagram credentials, API requests, or live data updates |
| Location, demographics, and follower-range filters | Not implemented | The working input is a category selection |
| Trained classification or regression models | Not implemented | Matching and ranking are deterministic rules, not trained ML models |
| Sentiment analysis, named-entity recognition, or topic modelling | Not implemented | These appear as general NLP discussion or proposed capability only |
| JavaScript-driven real-time interface | Not implemented | The current application is server-rendered Flask with CSS |
| Random data generation | Not used in this reconstruction | The repository keeps a fixed fictional dataset so results and tests are reproducible |

## Results that need correction or evidence

The report uses phrases such as “within milliseconds,” “parallel processing,”
“exceptional accuracy,” “high throughput,” “scalability,” and successful
benchmarking. No measured latency table, hardware specification, load-test
result, labelled evaluation dataset, accuracy metric, baseline comparison, or
reproducible experiment is provided. These statements must not be presented as
verified results.

For a final academic revision, either:

- add reproducible experiments with dataset size, hardware/software versions,
  test method, baseline, metrics, numeric results, and limitations; or
- rewrite the statements as objectives, design expectations, or future work.

The classification and regression diagrams should also be removed or labelled
as proposed work unless trained models, training data, evaluation metrics, and
source code are added.

## Repository reconstruction boundary

The repository is a professional reconstruction of the demonstrated core, not
an assertion that every sentence in the PDFs was implemented. The following
items were added during reconstruction: a modular application structure, fixed
fictional dataset, explicit scoring weights, validation, offline NLP fallback,
responsive interface, accessibility improvements, automated tests, CI,
community files, security guidance, and deployment configuration.

The current screenshots and routes therefore differ from the original academic
screenshots. That difference should be described as a later engineering update,
not silently presented as the original 2024 interface.
