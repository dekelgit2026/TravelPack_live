# Opportunity card: Business trip planner within policy

*Meeting 2 output · Travel / operations · fictional company: **Harbor & Pine**, 600 people, offices in Tel Aviv, London and New York. All data is anonymized.*

## The process today (as-is)
1. An employee emails the travel desk: where, when, why, and any constraints.
2. A travel coordinator (2 people) searches flights and hotels in the corporate booking tool, checks `travel-policy.md`, and emails back 2–3 options.
3. Usually there are 2–4 more emails about dates, times and hotel location.
4. The employee picks an option. If it's out of policy, the manager approves.
5. The coordinator books it in the booking tool. The booking tool sends the itinerary.

## Pain, with numbers (last quarter)
- **~260 trips a month.** About 80% are simple return trips: one city, 1–4 nights.
- **2 business days** on average from request to options; **3.4 emails** per trip.
- **22% of bookings are out of policy**, mostly because they're booked fewer than 14 days ahead or the hotel is over the cap. Managers approve after the fact.
- The coordinators spend **~70% of their time** on simple trips, and complex trips (multi-city, events, visas) wait.

## The AI-enhanced idea (to-be sketch)
The employee fills in a short request (a form or Slack). The system searches flights and hotels **through the booking tool's API**, checks each option against the policy, and returns 3 options with a clear policy status and price. The employee picks one. In-policy picks go to the coordinator for a one-click booking; out-of-policy picks go to the manager first. **Complex trips go straight to a coordinator.**

## Scores (Meeting 2)
| Business value | Complexity | Rough ROI | Priority |
|---|---|---|---|
| 3 / 5 | 3 / 5 | Coordinators' time moves to complex trips; fewer out-of-policy bookings | **Big bet (pilot)** |

**AI fit:** medium. Understanding a free-text request and explaining trade-offs suits an LLM. The search, the prices and the policy arithmetic must come from systems and rules, **never from the model's memory**.

## Risks we already know
- A wrong date or airport is expensive. Changing a ticket costs $150–$400.
- Prices change in minutes: options must be fetched live, not remembered.
- Duty of care: some destinations need a security approval first.
- Passport and loyalty numbers are personal data and must never reach the model.

## Data available
- `examples.csv`: 16 past requests, anonymized, with what was finally booked and the coordinator's notes.
- `travel-policy.md`: the travel policy (3 pages).
- The booking tool has a search API: flights, hotels, and booking with approval. It's a fictional system for this exercise.
