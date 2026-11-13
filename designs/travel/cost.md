# Cost estimate: Business trip planner within policy
Pack: travel · v1 · updated 2026-11-13 · Illustrative: check the provider's pricing page.

Prices used: $3 per million input tokens, $15 per million output tokens (illustrative). Arithmetic was run in Python.

## Inputs
| Input | Value | Source |
|---|---|---|
| Trips per month | 260, about 208 simple (80%) | Card |
| Peak volume | OPEN QUESTION; shown as 2x ASSUMPTION | none |
| Package call per simple trip | 1 call | ADR-001 |
| Slack call | ASSUMPTION: 1 per trip, 260 per month | none |
| Package call, input tokens | 2,278 = 800 instructions + 364 policy (1,457 chars / 4) + 114 form and request + 750 for 3 options + 250 outside options | Measured policy; the rest ASSUMPTION |
| Package call, output tokens | ASSUMPTION: 400 | Spec §4 |
| Slack call, tokens | ASSUMPTION: 1,050 in, 150 out | none |
| Time saved per simple trip | ASSUMPTION: 40 minutes of coordinator time | none |
| Loaded hourly cost | ASSUMPTION: $60/h | default |

## Calculation
| Item | Calculation | Result |
|---|---|---|
| Volume | 260 trips; 208 package calls + 260 Slack calls | 468 calls / month |
| Input tokens / month | 208 x 2,278 + 260 x 1,050 | 746,824 |
| Output tokens / month | 208 x 400 + 260 x 150 | 122,200 |
| Model cost / month | 746,824 x $3/M + 122,200 x $15/M | $4.07 |
| Safety margin x2 (retries, testing, growth) | $4.07 x 2 | **$8.15 / month** |
| **Cost per task** | $8.15 / 260 trips | **about $0.03 per trip** |
| Value: hours saved / month | 208 x 40 min / 60 | 139 hours |
| Value: $ / month | 139 h x $60 | about $8,320 |

At peak (2x, ASSUMPTION) the model cost is about $16 a month.

## Against ADR-001
ADR-001 sets no cost-per-trip target (OPEN QUESTION), so this cannot pass or fail yet. A candidate target for the architect to confirm: at most $0.50 per trip, which leaves a wide margin over the $0.03 estimate.

## What this estimate leaves out
Model cost is tiny. The real cost is likely elsewhere, and none of it is in the card:
- booking-tool API fees
- access to outside sources (search APIs, comparison sites)
- the form tool, orchestration and hosting
- the coordinator's review time in the first month (every trip is checked)
- the browser assistant for outside bookings: it takes many page steps per booking, so it is not the 1-call model above, and the cost per assisted booking is not estimated here

## What would change the cost by 10x
- Promoting the workflow to an agent: about 10 calls per trip with growing context takes the model cost to about $53 a month (6.5x here), and it varies per request.
- Putting a large policy or per-country rules in every prompt.
- A larger model on every call, including Slack.

## One cheaper option (not taken in v1)
Use a smaller model for the Slack status answers, or rule-built text for simple status replies. Cache the policy text in the prompt. Meeting 5 covers it.
