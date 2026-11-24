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


# --- Task 3: ingredient scaling ---
from main import scale_ingredient


def test_scale_ingredient_units():
    assert scale_ingredient("200 g flour", 2) == "400 g flour"
    assert scale_ingredient("1.5 cups milk", 2) == "3 cups milk"
    assert scale_ingredient("1/2 tsp salt", 3) == "1.5 tsp salt"
    assert scale_ingredient("1 1/2 cups sugar", 2) == "3 cups sugar"
    assert scale_ingredient("3 eggs", 0.5) == "1.5 eggs"
    assert scale_ingredient("salt to taste", 2) == "salt to taste"


def test_scaled_endpoint():
    rid = client.post(
        "/recipes", json={"title": "Bread", "ingredients": ["200 g flour", "pinch of salt"]}
    ).json()["id"]
    r = client.get(f"/recipes/{rid}/scaled?factor=2")
    assert r.status_code == 200
    assert r.json()["ingredients"] == ["400 g flour", "pinch of salt"]
    # stored recipe is untouched
    assert client.get(f"/recipes/{rid}").json()["ingredients"] == ["200 g flour", "pinch of salt"]


def test_scaled_bad_factor_and_missing_recipe():
    rid = client.post("/recipes", json={"title": "X", "ingredients": ["1 egg"]}).json()["id"]
    assert client.get(f"/recipes/{rid}/scaled?factor=0").status_code == 422
    assert client.get(f"/recipes/{rid}/scaled?factor=-1").status_code == 422
    assert client.get(f"/recipes/{rid}/scaled").status_code == 422
    assert client.get("/recipes/99999/scaled?factor=2").status_code == 404
