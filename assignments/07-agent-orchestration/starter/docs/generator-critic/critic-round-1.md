# Critic review: round 1 (branch w7-task-c-scaling)

Evidence: pytest gives 6 passed. Edge cases were run against the real `scale_ingredient` and the endpoint through TestClient.

## Scores
| Criterion | Score | Evidence |
|---|---|---|
| Correctness | 2/5 | Simple cases work ("200g flour", "1 1/2 cups", leading spaces, "pinch of salt", int display "400"). Three inputs produce silently wrong amounts or crash (MUST 1-3). |
| Tests | 3/5 | The happy path, an unmatched line, non-mutation of the stored recipe, 422 and 404 are covered with meaningful assertions. None of the broken inputs below is tested. |
| Clarity | 4/5 | Short, docstring present, regex commented, ponytail note on decimal output. Response shape gives no hint that the recipe was scaled (SHOULD 2). |

## MUST
1. **Ranges are half-scaled.** `scale_ingredient("2-3 eggs", 2)` returns `"4-3 eggs"`. Expected `"4-6 eggs"`, or leave the line unchanged. A wrong quantity is worse than an unscaled one. Fix: scale both ends of `N-M` / `N–M`, or skip the line when the quantity is followed by `-` and a digit. Add a test.
2. **Decimal comma gives a wrong number.** `scale_ingredient("1,5 l water", 2)` returns `"2,5 l water"`. Expected `"3 l water"` (or `"3,0"`). Only the `1` is matched and doubled. Fix: accept `\d+[.,]\d+` (normalize `,` to `.`), or refuse to scale when the number is followed by `,\d`. Add a test.
3. **A zero denominator causes a 500.** A stored ingredient `"1/0 cup"` makes `GET /recipes/{id}/scaled?factor=2` raise an unhandled `ZeroDivisionError`. Expected 200 with the line unchanged. Ingredients are user input, so this is a trust boundary. Fix: catch `ZeroDivisionError` (return the line as is), or use `[1-9]\d*` for denominators. Add a test.

## SHOULD
1. **Small results round to 0.** `("0.001 g yeast", 0.5)` gives `"0 g yeast"` and `("2 eggs", 1e-9)` gives `"0 eggs"`. A scaled ingredient should never read as "0 X". Use significant figures (e.g. `f"{float(qty):.3g}"`) instead of `round(..., 2)`, or keep the original if the result rounds to 0. A lower bound on factor (e.g. `ge=0.01`) also helps.
2. **Response shape.** Echo `"factor": factor` in the response so clients and caches know the data is scaled. Optional and in scope.
3. **Unicode fractions.** `"½ cup milk"` is left unchanged. That is safe, but it is common in real recipes. Mapping `½ ¼ ¾ ⅓ ⅔` to Fractions is cheap. Leave it if out of scope.
4. **Leading whitespace is dropped.** `"  200 g flour"` becomes `"400 g flour"`. This is harmless and arguably better. Note only.
5. **"0.33 egg" / "1 eggs".** Fractional counts and grammar (`("3 eggs", 1/3)` gives `"1 eggs"`) are acceptable for this scope. Do not fix pluralization.

## Not issues
`"2x400g tins"` becomes `"4x400g tins"`, which is correct. `factor=1000` works. `factor=0`, `factor=-1` and a missing factor return 422. The stored recipe is not mutated.

VERDICT: REVISE
