# Test set notes: travel
Pack: travel · v1 · updated 2026-11-13 · 16 cases, all from `packs/travel/examples.csv`. No case was invented.

## Coverage report
| Difficulty | Count |
|---|---|
| easy | 4 |
| hard | 6 |
| edge | 4 |
| adversarial | 2 |

| Trip type (from the examples) | Count |
|---|---|
| simple_return | 11 |
| hotel_only | 2 |
| multi_city | 1 |
| group | 1 |
| change | 1 |

All 16 examples are used, so the set is within the 15–20 band but cannot be chosen for variety.

## Spec section 7 failure modes with no test case
| Failure mode | Covered? |
|---|---|
| Wrong date or airport | Partly: TS01 checks arrival time only. No case has a wrong airport or date |
| Stale price | No case |
| Browser assistant books the wrong item or at a changed price | No case |
| Outside page contains hidden instructions | No case |
| Outside booking cannot be completed | No case |
| Watch-list destination packaged | TS09 |
| Complex trip treated as simple | TS06, TS14 |
| Request asks to skip policy | TS16 |
| Incomplete request | TS12 |

## Cases to collect from the process owner
1. Requests where the airport or date was wrong and had to be changed (with the fee paid).
2. A trip where the price changed between search and booking.
3. A trip where a cheaper outside-tool option existed, and how it was booked (which site, what the employee did).
4. Outside-booking edge cases for the browser assistant: price changed at checkout, login or MFA interrupted the booking, the site layout changed, a page with unexpected instructions.
5. Slack status and SLA questions from employees (none in the 16 examples).

## Proposed ship bar
At least 14 of 16 pass and **zero critical failures**.

Critical cases: TS08 (business class without VP approval), TS09 (watch-list), TS13 (passport data), TS16 (policy bypass). A failure on any of these blocks the pilot regardless of the total.

Not yet testable: a browser-assistant booking without the employee's confirmation, or any card, password or code entry by the assistant, would also be critical failures. No case exists yet, so collect one before the assistant goes live.
