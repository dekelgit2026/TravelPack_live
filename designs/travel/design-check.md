# Design check: travel
Pack: travel · v1 · re-run 2026-11-13 · Read-only review. No design file was changed by this check.
Resolved since the last check: seniority rules removed from spec, architecture and test notes; outside-tool bookings now have an owner (the employee, with a browser assistant).

## 1. Completeness
All present: `spec.md`, `ADR-001.md`, `architecture.md`, `cost.md`, `testset.csv` (plus `testset-notes.md`).

## 2. Consistency checks
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Spec metrics match ADR targets | ⚠️ | The 70% criterion and the 10-minute latency match. Both are assumptions. Cost is open in both |
| 2 | Cost per task meets the ADR target | ⚠️ | ADR-001 has no cost target. cost.md ($0.03 per trip) leaves out the browser assistant, which takes many page steps per booking |
| 3 | Spec §5 human role = the workflow's human step | ✅ | Coordinator and manager review at once (station 5). The outside path has its own human step: the employee confirms the item and total |
| 4 | Every failure mode has a test or a case to collect | ✅ | New browser-assistant failure modes are listed as "No case" and under cases to collect #4 |
| 5 | Pattern matches the architecture | ⚠️ | Rung 4, but the browser assistant is an agent-like step. ADR-001 gives the reason (outside pages differ by site), bounds it, and sets revisit triggers. Tools match the spec |
| 6 | "It will NOT…" is enforced | ✅ | Booking and card: permissions table and G. Unconfirmed or card, password and code entry: G, hard stops. Company card and email: G |
| 7 | Real examples only, with hard cases | ✅ | 16 of 16 from examples.csv; 6 hard, 4 edge, 2 adversarial |

## 3. Red flags
- **Money moved by an AI, with a human step:** the browser assistant spends the employee's own money. The per-booking confirmation makes it acceptable, but it is the riskiest step and **has no test case**.
- **Metric without a baseline:** AI cost per trip has no baseline and no target.
- **Thin adversarial coverage:** 2 of 16 cases are adversarial, and none covers hidden instructions on an outside page.
- Clear: no personal data in any file; "It will NOT…" present; test cases are all real; no multi-agent design.

## 4. Verdict
**The weakest box:** Tools and guardrails (T, G) for the browser assistant: no test cases, and reimbursement and privacy are unanswered.
**One question for the process owner:** is an outside-tool booking reimbursed (and do policy rules T1-T5 apply), and is it acceptable for an assistant to act in an employee's personal accounts?

**Fix first:**
1. Collect test cases for the assisted booking: no confirmation (critical), changed price, interrupted login, hidden page instructions.
2. Set a cost-per-trip target in ADR-001, including assisted bookings.
3. Name the process owner and answer the reimbursement and privacy questions.
