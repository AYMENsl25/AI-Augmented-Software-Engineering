# Tasks

These are small, independent improvements to the link shortener. Complete **one** for this assignment.

Whichever task you choose, add behavioral tests for the successful behavior and at least one failure or edge case.

1. **Custom alias** — allow `POST /shorten` to accept an optional `alias`; use it as the code if it is available, otherwise return 409.
2. **Click counter** — track how many times each code has been visited; expose `GET /stats/{code}` returning `{ "url": ..., "clicks": N }`. Return 404 for an unknown code.
3. **Expiry** — accept an optional positive `expires_in_days`; return 410 for an expired link and reject invalid expiry values.
