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


def test_scale_ranges():
    assert scale_ingredient("2-3 eggs", 2) == "4-6 eggs"
    assert scale_ingredient("1 – 1 1/2 cups milk", 2) == "2–3 cups milk"


def test_scale_decimal_comma():
    assert scale_ingredient("1,5 l water", 2) == "3 l water"


def test_scale_zero_denominator_unchanged():
    assert scale_ingredient("1/0 cup", 2) == "1/0 cup"
    rid = client.post("/recipes", json={"title": "Z", "ingredients": ["1/0 cup"]}).json()["id"]
    r = client.get(f"/recipes/{rid}/scaled?factor=2")
    assert r.status_code == 200 and r.json()["ingredients"] == ["1/0 cup"]


def test_scale_small_never_zero():
    assert scale_ingredient("0.001 g yeast", 0.5) == "0.0005 g yeast"
    assert scale_ingredient("1/3 tsp salt", 0.01) == "0.0033 tsp salt"


def test_scaled_echoes_factor_and_min_factor():
    rid = client.post("/recipes", json={"title": "F", "ingredients": ["2 eggs"]}).json()["id"]
    assert client.get(f"/recipes/{rid}/scaled?factor=1.5").json()["factor"] == 1.5
    assert client.get(f"/recipes/{rid}/scaled?factor=0.001").status_code == 422


def test_scale_thousands_separators():
    assert scale_ingredient("1,500 g flour", 2) == "3000 g flour"
    assert scale_ingredient("12,000 mg salt", 0.5) == "6000 mg salt"
    assert scale_ingredient("1,5 l water", 2) == "3 l water"
    assert scale_ingredient("1,25 kg sugar", 2) == "2.5 kg sugar"
    assert scale_ingredient("1.000,5 g flour", 2) == "1.000,5 g flour"
    assert scale_ingredient("1.2.3 g flour", 2) == "1.2.3 g flour"
