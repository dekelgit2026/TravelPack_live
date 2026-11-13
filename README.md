# Travel Pack: business trips planned within policy

An AI feature design for **Harbor & Pine**, a fictional company with 600 people and offices in Tel Aviv, London and New York. An employee fills in a short form, the system searches live and checks every option against the travel policy, and a coordinator books it with one click. The repo holds the design, the prompt layer, the eval evidence and an interactive demo.

**Live demo:** https://dekelgit2026.github.io/TravelPack_live/ (GitHub Pages, from `/docs`)

## What the page shows
| Tab | What it is |
|---|---|
| Overview, Spec, Pattern, Workflow, Architecture, Cost, Test set, Design check | The Solution Design v1 files, made interactive |
| **Live demo** | Run the six-station workflow on mock requests, with the architecture beside it and every MCP or API call marked |
| **Private trip** | A vacation planner with flights, stays and things to do, a budget, a mock booking, a calendar entry and a vacation ledger. Mock data, or a dated snapshot of real search results |
| **Eval lab** | Score prompt versions v1, v2 and v3 on Haiku and Sonnet. Free mock replay or real API calls, an approved baseline, mock-vs-actual comparison, visible test cases and failures, and a cost-saving panel |

## What is in the repo
| Folder | Contents |
|---|---|
| `packs/travel/` | The inputs: opportunity card, the travel policy, 16 anonymized real examples |
| `designs/travel/` | Spec, ADR-001 (pattern), ADR-002 (model choice), architecture, cost, test set, design check |
| `prompts/travel/` | System prompts v1 to v3, output schema, runnable cases, the version log |
| `results/travel/` | Every recorded eval run and the scoreboard |
| `evalkit/` | The eval runner, the local server, the site-data builder, token prices |
| `prototype/`, `docs/` | The page. `docs/` is the published copy |

## Run it on your computer
Python 3.10+ only, nothing to install.
```
python evalkit/serve.py          # then open http://127.0.0.1:8765/trip-planner.html#eval
```
**Secret mode.** To use real API calls, put `ANTHROPIC_API_KEY=...` in a file named `.env` next to `.env.example` (a dev key with a spend limit). The server reads it and calls the API itself, so the key is never sent to the page, a response or a file. `.env` is git-ignored. A public page can never hide a key, so the live site offers the free mock, plus an optional paste-your-own-key field that stays in the tab's memory.

Refresh the published copy after a new run:
```
python evalkit/build_site_data.py travel --site
```

## Honest limits
- The company, people, prices and bookings in the demo are fictional. The Lisbon snapshot in the Private trip tab is real search output, dated, and may be out of date.
- The eval has 11 cases. One case is about 9 points, so a one-case gap can be noise. Both prompt versions are at the ceiling, so the score cannot yet separate them on policy safety.
- The design check verdict is **Fix first**: see `designs/travel/design-check.md`.
