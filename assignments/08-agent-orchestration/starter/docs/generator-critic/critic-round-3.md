# Critic review: round 3 (commit 1263821)

Evidence: pytest gives 12 passed. All round-1 and round-2 probes and the new ones were run against the real code.

## Round-2 MUST: fixed
- "1,500 g flour" x2 gives "3000 g flour". "12,000 g" gives "24000 g".
- "1,500-2,000 g" gives "3000-4000 g". "1,5-2 l" gives "3-4 l". "2,5-3,5 dl" gives "5-7 dl".
- Ambiguous or malformed numbers are left unchanged: "1.000,5 g", "1,500.5 g", "1.2.3 g".
- Trailing punctuation is safe: "200, sifted" gives "400, sifted" and "200. g" gives "400. g".

## Regressions: none
"200g flour" gives "400g flour". "2-3 eggs" gives "4-6 eggs". "2 - 3" and "2–3" work. "1/2-1 cup" gives "1-2 cup". "1,5 l" gives "3 l". "1/0 x" is unchanged and the endpoint returns 200. "0.001 g" x0.5 gives "0.0005 g". "1 1/2 cups" gives "3". "1/2 tsp" x3 gives "1.5". Leading spaces, "salt to taste", "2x400g tins", x1000 and "10-12 min" x0.5 are all correct. factor 0.005, nan and abc return 422, 0.01 returns 200, an unknown id returns 404, and factor is echoed.

## On the "1.500" limitation
"1.500 g" x2 gives "3 g", because it is read as 1.5. I judge this **acceptable scope**. The string is truly ambiguous without locale: "1.500 kg" in US/UK style is 1.5 kg. The common reading of a period is a decimal point, and the alternative breaks valid inputs. Skipping the line would also break them. Fixing it properly needs a locale parameter, which is outside this task. The generator documented it. "1,50 g" reading as 1.5 is the same reasoning and is correct for European decimal commas.

## Scores
| Criterion | Score | Evidence |
|---|---|---|
| Correctness | 4/5 | Every realistic input in the probe set is handled or safely left alone. The only remaining wrong output comes from a truly ambiguous locale case. |
| Tests | 4/5 | 12 tests cover ranges, decimal and thousands commas, ambiguity, 1/0, tiny results, validation and non-mutation. |
| Clarity | 4/5 | Small helpers (`_parse`, `_scale`, `_fmt`). The parse rules and the known ceiling are commented. |

## MUST
None.

## SHOULD
1. Add a one-line test pinning "1.500 g" as 1.5, so the documented limitation is a tested decision and not an accident.
2. Unicode fractions ("½") and pluralization ("1 eggs") are still unhandled. Fine for scope.

VERDICT: APPROVE
