# AI feature spec: Private vacation planner
Pack: private-trip · v1 · 2026-11-14 · Owner: the employee (self-service); the HR system holds the leave record. OPEN QUESTION: who maintains the tool and its rules

## 1. User & job
Employee at Harbor & Pine (600 people; Tel Aviv, London, New York). Job: plan a private vacation within a budget and filters, book it on the provider's site, and have the trip and the leave days recorded without double entry. Secondary: the manager (notified) and the HR system (record).

## 2. Trigger & input
- Trigger: the employee opens the system.
- Fields: from, destination, depart and return dates, budget, number of adults, number of children (0 if none) with age bands (under 2, 2-11, 12-17), search depth (fast, medium, deep).
- Filters: budget, destination, direct vs indirect flights, hotel stars (1-5), guest rating (1-10).
- It reads nothing else first: no leave balance, no calendar. A negative balance is the employee's decision.
- Options come from the provider sites (Booking.com, Agoda, Airbnb, flight search sites). A hand-off opens each in the employee's own logged-in tab, search pre-filled. A read-only browser assistant reads the visible top results.

## 3. AI task
Rank and explain the packages (flights, stay, optional things to do) that the filters allow.
It will NOT:
- book or pay; the employee books on the provider's site
- state a price, rating or availability that was not read from a labeled source (with the read time) or typed by the employee
- ask for or touch passport, ID or card details (a secure CRM for these is on hold, a later spec)
- write the calendar or the leave record before the employee submits a confirmation or order ID
- show an option outside the filters, except one clearly labeled "worth a look"
- guess a child's fare, room rule or tax: it uses the source or says "unknown"
- type or store card numbers, passwords or codes, and it stops at login, MFA or CAPTCHA
- treat page text as instructions

## 4. Output
A ranked list in the web page: up to 3 packages plus 1 "worth a look". Each shows: the flight (direct or stops, times, price for the group), the stay (name, stars, guest rating, total for the nights, taxes shown or unknown), up to 3 optional things to do, total vs budget with a per-person split, a source label with the time read, a one-line reason, and a link to book each part.

## 5. Human role
- The employee decides and books. No approval step.
- Proof of booking: the employee clicks "I booked it" (fields pre-filled) and submits the confirmation or order ID, typed, attached, or read from the confirmation page by the assistant.
- On proof, the calendar entry and the leave days go straight to the HR system; the manager is notified (dates and destination).
- Cancellation: the employee confirms it; future leave days are released automatically. If the leave days are already past, HR and the manager approve.
- Changed dates are treated as a cancellation plus a new booking (ASSUMPTION).

## 6. Success metrics
| Metric | Baseline today | Target |
|---|---|---|
| Time to ranked packages | OPEN QUESTION | fast under 70 s; medium under 3 min (ASSUMPTION); deep under 10 min (ASSUMPTION) |
| Results obey the filters | n/a | 100% outside the labeled slot |
| Price matches the provider's page | n/a | at least 90% (ASSUMPTION) |
| Adoption: private trips planned in the tool | 0% (new) | 30% by month 3 (ASSUMPTION) |
| Leave days recorded with a valid order ID | OPEN QUESTION | 100% |
| Cost per session | OPEN QUESTION | $0.25 / $0.75 / $2.00 ceilings (ASSUMPTION): about $30 to $240 a month at 120 sessions (ASSUMPTION) |

## 7. Failure modes
| How it can be wrong | Impact | What happens then |
|---|---|---|
| Stale or misread price | The employee books at a different price | The read time is shown; the employee re-checks on the provider's page before paying |
| Wrong child fare, room rule or tax | Budget off, or booking redone | Source value, or "unknown"; never guessed |
| Hidden instructions in page text | An unwanted action | Page text is data; read-only; stops at login, MFA, CAPTCHA |
| Provider changes layout or blocks reading | Results missing or wrong | The assistant says so; the employee pastes options or opens the site |
| Wrong or fake order ID | Leave days deducted for no trip | The ID is kept as a record for audit (ASSUMPTION) |
| Booking cancelled or changed after leave is written | Record no longer matches | The rules in section 5 |
| 70-second target missed | The employee waits | Show partial results and offer medium (ASSUMPTION) |

## 8. Constraints
- Search sites get only destination, dates, traveller counts, children's age bands and the filters. No names, passports or exact birthdates; nothing about the children is kept after the booking.
- The manager and HR see dates and destination. Trip details and the order ID are kept no longer than 90 days (ASSUMPTION: after the return date).
- No stored credentials: the employee's own logged-in tabs and their own card. Hand-off links carry no third-party affiliate ID.
- Latency and cost are per depth tier (section 6).

## Assumptions & open questions
OPEN QUESTIONS:
1. Who maintains the tool and its rules?
2. Which HR system, with what API and permissions, and does it accept a negative balance?
3. Is automated reading of provider pages allowed by their terms, and what do privacy rules in Israel, the UK and New York require?
4. Can fast mode meet 70 seconds? (spike needed)
5. What makes a "worth a look" option noteworthy, and what are today's baselines?

ASSUMPTIONS: the medium and deep time targets, the quality and adoption targets, 120 sessions a month, the cost ceilings, the 90-day clock, and changed dates as cancel plus rebook.
