# Opportunity card: Private vacation planner (DRAFT)

*Drafted on 2026-11-14 from the design conversation, not a Meeting 2 output. Company: **Harbor & Pine** (fictional), 600 people, offices in Tel Aviv, London and New York. Nothing below is measured. Every gap is marked **ASSUMPTION** or **OPEN QUESTION** for the process owner. No examples exist yet.*

## The process today (as-is)
OPEN QUESTION: how do employees plan a private trip and tell the company today?
ASSUMPTION: the employee plans alone on public booking sites, pays with their own card, and files a leave request separately (form, email or HR system). The trip and the leave are recorded in two places.

## Pain, with numbers
No numbers yet. OPEN QUESTION: how many private trips and leave requests a month, how long planning takes, how often the leave record disagrees with the trip.
Pain we believe exists, to be confirmed: planning is scattered across sites; the leave days are entered twice; the manager and HR learn the dates late.

## The AI-enhanced idea (to-be sketch)
The employee writes a **destination, depart and return dates and a budget**. The system proposes two or three vacation packages (flights, stay, things to do) that fit the budget, with every price labeled by source. The employee picks one and **books on the provider's site with their own card** (hand-off links). After the booking is confirmed, the trip goes into the **employee's calendar**, the **working days are registered as vacation days** for the company's bookkeeping, and the **manager is notified** (no approval step in v1).

## Scores (Meeting 2)
OPEN QUESTION: not scored. Business value, complexity and priority need the process owner.

## Risks we already know
- **No self-serve live prices.** Kiwi, Booking.com, Skyscanner, Agoda and Tripadvisor offer their search APIs only to approved commercial partners, and some forbid caching or republishing prices. A live search needs a partner contract, or a different path (search links plus prices the employee types in).
- **Prices change in minutes.** Anything shown must be fresh, or labeled as an estimate or a dated snapshot.
- **Price meaning is unconfirmed:** total or per night, taxes and fees, currency, cancellation.
- **Private data.** A private trip is personal. What the company may store (calendar, vacation ledger, manager notice) needs HR and legal sign-off.
- **Leave rules differ by office:** workweek (Mon-Fri or Sun-Thu), public holidays, half days, and whether leave needs approval by law or policy.
- **Third-party affiliate links** must not carry someone else's affiliate ID.

## Data available
- **No examples yet.** OPEN QUESTION: collect 15 to 20 anonymized real private-trip or leave requests (destination type, length, budget, what was booked).
- A prototype, the Private trip tab: a dated Lisbon snapshot (5 Nov 2026), a fictional Barcelona set, and labeled estimates. It is one capture, not an example set.
- The company's vacation policy and balance source: OPEN QUESTION, not provided.
