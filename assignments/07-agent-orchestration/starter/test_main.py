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
