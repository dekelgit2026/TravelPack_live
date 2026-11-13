# evalkit: the runner

`run_eval.py` sends each case in `prompts/<pack>/cases.csv` to the model with your system prompt, checks the answer, and records the score, cost and latency. Python 3.10+, standard library only.

```
python evalkit/run_eval.py <pack> [--prompt v1] [--model haiku] [--judge] [--only T01,T15]
python evalkit/run_eval.py <pack> --engine baseline
python evalkit/run_eval.py <pack> --dry-run
python evalkit/run_eval.py <pack> --compare v1 v2
python evalkit/run_eval.py <pack> --compare haiku sonnet --prompt v2
```

| Option | What it does |
|---|---|
| `--prompt v2` | Reads `prompts/<pack>/system_v2.md` |
| `--model` | `haiku` (default), `sonnet`, `opus`, `fable`, or a full model id |
| `--engine baseline` | No model, no key: returns `baseline.json` for every case |
| `--dry-run` | Prints what the model would see for the first case. Sends nothing |
| `--judge` | Also runs `judge:` checks with a second model (`--judge-model`, default `sonnet`) |
| `--compare A B` | Two prompt versions or two models on the same cases |
| `--no-cache` | Turns prompt caching off, to measure what it saves |
| `--bar 80` | The ship bar in percent. A run is ready only at or above the bar **and** with zero critical failures |
| `--max-usd 0.50` | Budget guard for the run |

## What one call looks like
- **System:** your prompt, plus each `context:` document inside `<document>` tags. It is marked for caching: after the first call, the unchanged part is read from cache at a fraction of the price (it must be at least about 512 tokens to be cached).
- **Output shape:** `schema.json`, sent as a structured output, so the answer is always valid JSON with your fields.
- **User:** the case's `input`. Nothing else: the checks and expected outcomes are never sent.
- **Tools (optional):** `tools.json` lookups. The runner answers them from a local file and lets the model continue, for at most 3 rounds.

## What it records
`results/<pack>/<time>-<prompt>-<model>.json` holds every output, every check with what was seen, tokens, cost and latency. `scoreboard.md` gets one line per run. Commit both.

## Exit codes
`0` the run meets the bar · `1` it doesn't · `2` it couldn't run (missing file, no key, bad check, budget).

## Prices
`prices.json`, USD per million tokens, with the date they were checked. Costs in reports are estimates from token counts: the Console's Usage page is the bill.

## Serve and the Eval lab
`python evalkit/serve.py` serves the page and runs real evals with the key kept on your computer (secret mode). `python evalkit/build_site_data.py travel --site` refreshes `docs/` for GitHub Pages. See the repository README.
