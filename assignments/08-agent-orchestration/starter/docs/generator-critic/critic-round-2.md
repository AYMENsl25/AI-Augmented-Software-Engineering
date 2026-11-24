# Critic review: round 2 (commit 48e8b2d)

Evidence: pytest gives 11 passed. All round-1 probes and the new ones were run against the real code.

## Round-1 items
- MUST 1 (ranges): fixed. "2-3 eggs" becomes "4-6 eggs". "2 - 3" and "2–3" also work, and so do fraction ranges ("1/2-1 cup" becomes "1-2 cup") and "10-12 min" x0.5 ("5-6 min").
- MUST 2 (decimal comma): fixed. "1,5 l water" becomes "3 l water".
- MUST 3 (1/0): fixed. The line comes back unchanged and the endpoint returns 200.
- SHOULD 1: fixed. "0.001 g yeast" x0.5 gives "0.0005 g yeast". factor=0.005 returns 422 and 0.01 returns 200.
- SHOULD 2: done. The response includes "factor": 2.0.
- Regressions: none. "200g flour", "1 1/2 cups sugar", "1/2 tsp salt", "1.5 cups milk", "2x400g tins", "salt to taste", leading spaces and factor 1000 all behave as in round 1. nan, inf and abc return 422.

## Scores
| Criterion | Score | Evidence |
|---|---|---|
| Correctness | 3/5 | Every round-1 defect is fixed. The fix opened a new silent 1000x error on thousands separators (MUST 1). |
| Tests | 4/5 | 11 tests now cover ranges, decimal comma, 1/0, tiny results and factor echo. The thousands-separator case is missing. |
| Clarity | 4/5 | `_fmt` and `_scale` are small and well named. Comments state the intent and the known ceiling. |

## MUST
1. **A thousands separator is read as a decimal comma, so the amount is wrong by 1000x.** `scale_ingredient("1,500 g flour", 2)` returns `"3 g flour"`. Expected `"3000 g flour"`, or the line unchanged. `"1.000,5 g"` x2 gives `"2,5 g"`. Expected `"2001 g"` or unchanged. The generator lists this as a known limitation, but a silent 1000x error in a quantity is the same class of bug as round-1 MUST 2, and "1,500 g" is a common US recipe format. Minimal fix: treat a comma followed by exactly 3 digits (`\d{1,3}(,\d{3})+`) as a thousands separator, or don't scale ambiguous numbers (comma + 3 digits, or both `.` and `,`) and return the line unchanged. Add a test for "1,500 g flour".

## SHOULD
1. `"3-"` x2 gives `"6-"`. This is harmless and the input is unrealistic. Note only.
2. `"½ cup"` is still unchanged. This is safe and acceptable for scope.

VERDICT: REVISE
