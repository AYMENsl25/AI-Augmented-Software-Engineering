from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_get_recipe():
    r = client.post(
        "/recipes",
        json={"title": "Pancakes", "ingredients": ["flour", "milk"], "tags": ["breakfast"]},
    )
    assert r.status_code == 200
    rid = r.json()["id"]
    r2 = client.get(f"/recipes/{rid}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Pancakes"
    assert r2.json()["tags"] == ["breakfast"]


def test_list_recipes():
    client.post("/recipes", json={"title": "Toast"})
    r = client.get("/recipes")
    assert r.status_code == 200
    assert any(rec["title"] == "Toast" for rec in r.json())


def test_unknown_recipe_404():
    r = client.get("/recipes/99999")
    assert r.status_code == 404


# --- Task 2: tag filter ---


def test_tag_filter_exact_case_insensitive_and_trimmed():
    a = client.post("/recipes", json={"title": "TagOmelette", "tags": ["Breakfast2"]}).json()["id"]
    b = client.post("/recipes", json={"title": "TagSoup", "tags": ["dinner2"]}).json()["id"]
    ids = [r["id"] for r in client.get("/recipes", params={"tag": "  breakfast2 "}).json()]
    assert a in ids and b not in ids


def test_tag_filter_no_substring_match():
    rid = client.post("/recipes", json={"title": "TagWaffle", "tags": ["breakfast3"]}).json()["id"]
    assert rid not in [r["id"] for r in client.get("/recipes?tag=breakfast").json()]
    assert rid not in [r["id"] for r in client.get("/recipes?tag=break").json()]


def test_tag_filter_no_matches_returns_empty_list():
    r = client.get("/recipes?tag=no-such-tag-xyz")
    assert r.status_code == 200 and r.json() == []


def test_tag_filter_empty_means_no_filter():
    client.post("/recipes", json={"title": "TagUntagged"})
    assert client.get("/recipes?tag=").json() == client.get("/recipes").json()
    assert client.get("/recipes", params={"tag": "   "}).json() == client.get("/recipes").json()
