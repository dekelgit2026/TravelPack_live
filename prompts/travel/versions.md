# Prompt versions: travel
Never overwrite an old version: the scoreboard refers to it. A change goes into a new file.

| Version | Date | What it is | Status (scoreboard, Haiku) |
|---|---|---|---|
| v1 | 2026-11-13 | Numbered rules, one list. Policy attached. 3 examples (T02, T04, T11) | Scored: 9/11 (first checks), then 10/11 twice (corrected checks). No critical failures |
| v2 | 2026-11-13 | **Same schema, policy and examples as v1. One lever changed: how the rules are presented.** An ordered 4-step procedure; every flag checked on its own; the message must state what follows from each flag | Scored: 9/11 with TS16 failing (first checks), then 11/11 twice (corrected checks). Proposed pick in ADR-002 |
| v3 | 2026-11-13 | **v2 plus one lever: the input contract about dates.** The prompt says new trips come from a form that always supplies dates, so text that leaves them out is not a reason to ask. `missing_dates` and `ask_employee` apply only when the text says the dates are still to come | Scored: 11/11 twice, no critical failures, same cost per case as v2 (see result below) |

**Correction before the first live score (2026-11-13):** a pre-run check found that neither prompt named the `missing_dates` flag, which TS12 needs. It was added to both versions in the same words. v1 had no live score yet, so no scoreboard entry points to the earlier text.

## The v1 to v2 hypothesis (was PROPOSED; result below)
v2 was written before any live run, as a hypothesis. Lever: instruction structure only.
**Result:** the expected gain on TS16 did not appear, because v1 already set both flags there. The only difference between the versions is TS03, where v1 asked for a return date and v2 went ahead. See ADR-002: not decisive.

## The v2 to v3 hypothesis (PROPOSED)
**Why:** all the failures seen so far trace to the same behavior. The case inputs have no dates, and the model sometimes asks for them and sometimes proceeds (TS03 for v1, TS07 and TS16 earlier). In the real flow the form requires dates (station 1), so asking for them because the text omits them is noise. v3 states that input contract.
**Lever:** the dates contract only. v3 differs from v2 in exactly three lines (the "What you get" paragraph, Step 1, and the `missing_dates` bullet). Schema, policy, examples, cases and model are identical.
**Expected to help:** TS03, and the stability of TS07, TS08, TS10, TS14 and TS16 (fewer `ask_employee` and `missing_dates` where the text has no dates).
**Must not break:** TS12 ("I'll send dates later") has to stay `ask_employee` with `missing_dates`.
**Could get worse:** a Slack request with no dates at all would no longer be asked for them. The design sends new trips through the form, so this is accepted, but it is a behavior change to confirm with the process owner.
**Not a fix for the real weakness:** the eval cannot yet tell the versions apart on policy safety. More hard cases from real data are needed.

**Result (2026-11-13, two rounds on Haiku, `--compare v2 v3`):**
- Both versions scored 11/11 in both rounds, with no critical failures. No case flipped between pass and fail. Cost per case was identical on the scoreboard ($0.00015, then $0.00011); median latency was lower for v3 in both rounds (1284 vs 1521 ms, 1257 vs 1472 ms).
- The lever worked on behavior: over the 22 answers per version, `ask_employee` fell from 5 (v2) to 3 (v3), and the `missing_dates` flag from 7 to 4. TS08 and TS10, where v2 added `missing_dates`, no longer did under v3.
- The must-not-break case held: TS12 returned `ask_employee` with `missing_dates` in all four answers.
- Two of v3's four `missing_dates` flags are the correct TS12 ones; the other two were not traced to a case.
- Because both versions are at the ceiling, the score cannot show v3 is better. The evidence for v3 is behavior closer to the design (the form supplies dates), not a higher score.

## How to compare
```
python evalkit/run_eval.py travel --compare v2 v3
```
Change one thing at a time. After the prompt is chosen, compare models with it: `--compare haiku sonnet --prompt <winner>`.

## Limits of this eval
- 11 cases: one extra pass or fail moves the score by about 9 points, so treat a 1-case difference as noise. Run each version twice and look for cases that change between runs.
- Two critical cases (TS08, TS16) decide readiness, not the percentage.
- The model's main job in the design (explaining 3 live options) has no cases yet.
- TS09 (watch list) and TS13 (passport data) are tested at the rules layer, not here.
