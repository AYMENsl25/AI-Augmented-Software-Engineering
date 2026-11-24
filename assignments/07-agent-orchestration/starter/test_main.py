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


# --- Task 1: shopping list ---
def _mk(ings):
    return client.post("/recipes", json={"title": "x", "ingredients": ings}).json()["id"]


def test_shopping_list_merges_and_dedupes():
    a = _mk(["Flour", "milk", " eggs "])
    b = _mk(["flour ", "Butter", "MILK"])
    r = client.get(f"/shopping-list?ids={a},{b},{a}")
    assert r.status_code == 200
    assert r.json() == {"recipe_ids": [a, b], "items": ["Flour", "milk", "eggs", "Butter"]}


def test_shopping_list_missing_or_empty_ids():
    assert client.get("/shopping-list").status_code == 400
    assert client.get("/shopping-list?ids=").status_code == 400


def test_shopping_list_non_integer():
    r = client.get("/shopping-list?ids=1,abc")
    assert r.status_code == 400 and "abc" in r.json()["detail"]


def test_shopping_list_unknown_ids():
    a = _mk(["salt"])
    r = client.get(f"/shopping-list?ids={a},9998,9999")
    assert r.status_code == 404 and "9998" in r.json()["detail"] and "9999" in r.json()["detail"]

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
