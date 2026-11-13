# AI feature spec: Business trip planner within policy
Pack: travel · v1 · updated 2026-11-13 · Owner: OPEN QUESTION

## 1. User & job
Employee at Harbor & Pine. Job: get from trip request to a bookable, in-policy trip fast, instead of 2 days and 3.4 emails. Secondary users: coordinator (validates and books), manager (signs off the budget).

## 2. Trigger & input
- New trip: a structured form. Required fields: destination, dates, purpose, meeting place, traveller profile ID. (ASSUMPTION: exact field list.)
- Status, SLA and urgent changes: free-text Slack.
- From the booking tool: live flight and hotel search, traveller profile (passport and visa as pass/fail flags only), trip history.
- The AI never receives passport numbers, dates of birth or loyalty numbers.

## 3. AI task
Classify the request as simple or complex, then for a simple one assemble a bookable package (flights, hotel, total price) from live search results. Sub-tasks: draft a plain-language explanation of the options and trade-offs (e.g. "Saturday stay saves $240"), answer Slack status and SLA questions from booking-tool data, and, for an outside-tool option the employee picks, ask "Can I book this?" and hand that one booking to a browser assistant (see section 5).

It will NOT:
- charge a card or book anything in the booking tool; only a coordinator's click does, after the required approvals are recorded (T8)
- state a price or schedule that did not come from a live search; outside-tool options are allowed only when labeled "outside booking tool, unverified" with a link to the source site
- handle passport, date of birth or loyalty numbers (T7)
- auto-package or auto-book a watch-list destination (T6); send to security
- skip a policy check because the requester asks (T16)
- book an outside-tool option without the employee's explicit confirmation of the item and total, every time
- type, store or read back card numbers, passwords or one-time codes; it uses only the login and saved payment method already in the employee's own browser, and stops at login, MFA, CAPTCHA, a new-card form or a changed price
- use the company card or a company email for an outside-tool booking

## 4. Output
- Simple trip: 3 options with price, policy status (T1-T5) and a short explanation, plus a package for the coordinator and, when out of policy, the manager.
- Outside options (flight and hotel comparison sites, direct partners): shown only if at least 15% or at least $300 cheaper than the best in-tool option, labeled, linked, and with a "Can I book this?" button.
- Complex trip (multi-city, group, event, visa, watch-list): routed straight to a coordinator with the request attached.
- Slack: a short answer with the trip's current status.

## 5. Human role
- Coordinator and manager see the package at the same time.
- Manager: budget sign-off. Only the manager approves out-of-policy picks.
- Coordinator: checks price range, dates and airports against the request, arrival time against the event, and direct vs. non-direct. Can override the AI's choice. Clicks to book in the booking tool.
- First month: the coordinator checks every trip.
- Outside-tool options: the employee books, with their own card and private email. The planner shows the item and total and asks "Can I book this?". After the employee confirms, a browser assistant (Claude in the browser) completes that one booking in the employee's own already-logged-in tab. No credentials or tokens are stored in the system, and no per-site MCP server is needed, so sites such as Agoda or Skyscanner can be used. If the assistant hits a login, MFA, CAPTCHA, new-card form or changed price, it stops and the employee finishes on the site. The coordinator does not book these.

## 6. Success metrics
| Metric | Baseline today | Target |
|---|---|---|
| Pilot success (exit criterion) | n/a | At least 70% of trips classified simple go through with no coordinator change; the rest need only minor edits |
| Request to options | 2 business days | ASSUMPTION: 10 minutes |
| Emails per trip | 3.4 | ASSUMPTION: under 1 |
| Out-of-policy bookings | 22% | ASSUMPTION: under 10% |
| Coordinator time on simple trips | ~70% | ASSUMPTION: under 30% |
| Adoption: simple trips using the form | 0% (new) | ASSUMPTION: 70% by month 3 |
| AI cost per trip | not in the card | OPEN QUESTION |

If the pilot criterion is met, phase 2 extends the AI to complex bookings.

## 7. Failure modes
| How it can be wrong | Impact | What happens then |
|---|---|---|
| Wrong date or airport | $150-$400 to change | Coordinator checks dates and airports before booking |
| Stale price | Wrong budget sign-off | Prices fetched live; re-fetched at the click |
| Browser assistant books the wrong item or at a changed price | The employee's own money, hard to undo | Item and total confirmed just before the final click; stops if the price differs; employee checks the confirmation email |
| Outside page contains hidden instructions | Wrong action or data leak | Page content treated as data; allowlisted sites only; never enters card, password or codes; stops on anything unexpected |
| Outside booking cannot be completed | Delay | The assistant stops and the employee finishes on the site, or picks an in-tool option |
| Watch-list destination packaged | Duty-of-care breach | Hard rule: sent to security, never packaged |
| Complex trip treated as simple | Bad itinerary | Coordinator catches it; route to a coordinator when in doubt |
| Request asks to skip policy (T16) | Policy bypass | Checks always run; request noted |
| Incomplete request (T12) | Delay | Form blocks the search until required fields are filled |

## 8. Constraints
- Data: passport, birth date and loyalty numbers stay in the booking tool profile and never reach the model. Visa and passport-validity checks return pass/fail only.
- Outside-tool bookings use the employee's own login, card and private email in their own browser. Nothing is stored by the system.
- Prices are live from the booking tool, or labeled outside sources.
- Allowed outside sites: ASSUMPTION: the named comparison sites and direct partners only.
- Latency: ASSUMPTION: options in minutes, not days.
- Budget: OPEN QUESTION.
- Regulation: duty of care (T6).

## Assumptions & open questions
OPEN QUESTIONS:
1. Who owns the process (name or role)?
2. Is an outside-tool booking reimbursed, and do policy rules T1-T5 still apply to it?
3. How is the booking handed to the browser assistant (a webhook or a direct hand-off), and which sites are allowed?
4. Is it acceptable for the assistant to act in an employee's personal accounts and see those pages (privacy review)?
5. What are the AI cost-per-trip target and the budget?
6. What is the exact list of required form fields?

ASSUMPTIONS: the targets marked above (all except the pilot exit criterion), the field list and the allowed-sites list.
