# Tasks

Independent tasks, safe to run in parallel across agents / git worktrees.

1. **Shopping list** — `GET /shopping-list?ids=1,2,3` merges the ingredients of the
   given recipes into a de-duplicated list.
2. **Tag filter** — `GET /recipes?tag=breakfast` returns only recipes with that tag.
3. **Ingredient scaling** — `GET /recipes/{id}/scaled?factor=2` returns the recipe with
   quantities scaled (assume ingredients like "200 g flour").
4. **Favorites** — add a `favorite` boolean and `POST /recipes/{id}/favorite` toggle.
