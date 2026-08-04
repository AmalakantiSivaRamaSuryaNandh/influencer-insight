def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Find the creator who leads their niche" in response.data


def test_search_page_and_report_compatible_alias_load(client):
    assert client.get("/search").status_code == 200
    assert client.get("/index").status_code == 200


def test_valid_category_returns_highest_ranked_match(client):
    response = client.post("/search", data={"category": "technology"})

    assert response.status_code == 200
    assert b"Neha Kulkarni" in response.data
    assert b"29,670" in response.data
    assert b"Other strong matches" in response.data


def test_category_is_trimmed_and_case_insensitive(client):
    response = client.post("/search", data={"category": "  TECHNOLOGY  "})

    assert response.status_code == 200
    assert b"Neha Kulkarni" in response.data


def test_blank_category_is_rejected(client):
    response = client.post("/search", data={"category": ""})

    assert response.status_code == 400
    assert b"Please choose an influencer category" in response.data


def test_unknown_category_is_rejected(client):
    response = client.post("/search", data={"category": "astronomy"})

    assert response.status_code == 400
    assert b"Please choose one of the available categories" in response.data


def test_category_with_symbols_is_rejected(client):
    response = client.post("/search", data={"category": "tech<script>"})

    assert response.status_code == 400
    assert b"only letters, spaces, and hyphens" in response.data


def test_methodology_page_explains_assumption(client):
    response = client.get("/methodology")

    assert response.status_code == 200
    assert b"Implementation assumption" in response.data
    assert b"followers" in response.data


def test_health_endpoint_reports_dataset_size(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "influencers": 24}


def test_not_found_page(client):
    response = client.get("/not-a-real-page")

    assert response.status_code == 404
    assert b"That page is not in this dataset" in response.data
