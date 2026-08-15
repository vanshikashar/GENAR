# GenAR AI Engineering Challenge — Bisoprolol PADER (Version 0)

## How to run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...        # only needed for live LLM calls
python src/generate_report.py path/to/Bisoprolol_icsr_sample_1068rows.xlsx
```

This produces `report_output.md`, `analysis_output.json`, and
`review_state.json`. Run with `--offline` to execute the full pipeline
without an API key (each section renders as its raw evidence packet instead
of LLM prose — useful for verifying grounding end to end without spending
API calls).

`report_output.md` in this submission was produced by
`src/fill_sample_narratives.py`, which uses the exact same
`analysis.py` output and the exact same prompts as `generate_report.py`; the
section text was written directly against those packets rather than a live
API call, because this build environment has no network access. Running
`generate_report.py` with a real key reproduces the same shape for real,
one `claude-sonnet-4-6` call per section.

## Architecture

See `architecture.md` for the diagram. In short:

```
data -> analysis.py (deterministic) -> analysis_output.json
     -> 6 scoped evidence packets -> 6 small Claude calls
     -> review_state.json (human gate) -> report_output.md
```

## Where AI is used vs. deterministic code, and why

**Deterministic (Python/pandas), never the LLM:**
- Deduplicating 1,068 rows to 1,024 unique cases
- Every count: serious/non-serious, seriousness sub-criteria, age/sex/country
  breakdowns, top reactions, outcomes, 15-day alert counts, monthly trend
- The case index table

**LLM (Claude), one call per section:**
- Turning a JSON block of already-correct numbers into a readable paragraph
  in a consistent regulatory tone

The rule I used: if Python can compute it exactly, Python computes it. The
model's job is narrowly "write this up," not "figure out the numbers" —
an LLM doing arithmetic over 1,000+ rows is slower, non-reproducible, and
unauditable compared to `pandas.value_counts()`. This is also why each
section gets a *scoped* packet (see `prompts/sections.py`) instead of the
full analysis dump — the model literally cannot cite a number it wasn't
given, which is the actual grounding mechanism, not a prompt instruction
asking it to "only use real data."

## Prompts / context templates

`prompts/system.txt` — one shared system prompt (hard rules: only use
packet data, no causal conclusions, state nulls explicitly, plain prose).

`prompts/sections.py` — one packet-builder + one instruction string per
section. Example (Serious Cases / 15-Day Alerts):

```python
def alerts_packet(a):
    return {
        "reporting_period": a["reporting_period"],
        "alert_15day": a["alert_15day"],
        "case_volume": a["case_volume"],
    }

ALERTS_INSTRUCTIONS = (
    "State how many cases met expedited (15-day alert) criteria and, of "
    "those, how many were fatal. If nearly all serious cases also meet "
    "alert criteria, state that plainly as an observation about this "
    "dataset rather than a signal."
)
```

The system prompt carries rules that apply to every section (grounding,
tone, null-handling). Instructions specific to one section's content live
next to that section's packet builder, not in the system prompt — so a
section's rules are easy to find and change without touching the others.

## How the system stays grounded

Every number in `report_output.md` traces to `analysis_output.json`, which
is produced entirely by `src/analysis.py` (pure pandas, no LLM). Each
section's LLM call receives *only* the slice of that JSON relevant to it
(see `prompts/sections.py`) — never the raw dataframe, never the full
analysis dict. The system prompt forbids introducing any number, name, or
conclusion not present in the packet. This is checkable mechanically: diff
the numbers in a generated paragraph against the packet it was given.

## How I'd evaluate this at scale (1,000 reports, not one)

- **Numeric grounding check (automatable):** regex-extract every number in
  each generated section, verify it appears in that section's evidence
  packet. Flag any that don't — this catches hallucinated figures
  cheaply and does not require another LLM call.
- **Conclusion-leakage check:** a cheap classifier/rule pass over generated
  text for causal language ("caused by," "confirms," "safety signal")
  that isn't licensed by the packet — the Starter Guide's
  observation-vs-conclusion distinction is exactly what this checks.
- **Section completeness:** every report has all required sections, no
  section is empty, and `review_state.json` has no `"pending"` entries
  before a report counts as final.
- **Spot-check sampling:** a human reviewer reads a random 2-5% sample in
  full against the source data monthly, to catch grounding failures the
  automated checks weren't designed to catch.
- **Regression on the analysis layer:** since `analysis.py` is pure
  functions on a dataframe, it gets ordinary unit tests (e.g. a synthetic
  10-row dataframe with known answers) — cheaper and more reliable than
  testing generated prose.

## Human control

`review_state.json` is the gate: every section starts `"pending"`; a
reviewer (today: editing the JSON directly) sets each to `"approved"` or
`"flagged"`. A minimal real UI would be one table — section name, generated
text, packet it was shown, and an approve/flag toggle — reading and writing
that same file. `report_output.md` in this submission has all sections
marked `"approved"` in `review_state.json`, standing in for that review step.

## Known limitations

- **No SOC-level reaction grouping** — the dataset has no MedDRA System
  Organ Class field, only Preferred Term. Per the Starter Guide, I didn't
  infer one; the report explicitly states this rather than guessing.
- **No expectedness/labeling comparison** — no product label/CCDS was
  supplied, so "labelled vs. unlabelled" isn't computed anywhere here (the
  sample reference report has this; this dataset doesn't support it).
- **No history-of-actions data** — the report states this explicitly per
  section rather than leaving it blank or inventing content.
- **Outcome field is per-case, first-listed value** — some cases have
  multiple stacked reaction/outcome values in one cell (e.g.
  `"recovered/resolved,recovered/resolved"`); I treat the case's outcome
  field as-is rather than trying to split it further. A production version
  would need a clearer per-reaction outcome model.
- **Country: `occurcountry` chosen over `primarysource_reportercountry`**
  — noted in the report's data note, per the Starter Guide's callout that
  the two occasionally differ.
- **This submission's `report_output.md` wasn't produced by a live API
  call** (no network in this build environment) — see "How to run it"
  above for exactly how to reproduce it for real.
- **No retry/rate-limit handling** on the Claude calls beyond a bare
  try/except fallback to raw evidence — fine for 6 calls, would need real
  handling at the "1,000 reports" scale referenced in the evaluation
  question.

## Models used

Designed for `claude-sonnet-4-6` via the Anthropic Messages API — one call
per section, ~600 max tokens each, no tool use (nothing in this pipeline
needs a tool call; the "tool" is the deterministic Python layer feeding the
model a packet).

## Files

```
src/analysis.py              deterministic analysis (pandas only)
src/generate_report.py       orchestrator: packets -> LLM -> review gate -> report
src/fill_sample_narratives.py  produces this submission's report_output.md
prompts/system.txt           shared system prompt
prompts/sections.py          per-section packets + instructions
report_output.md             generated report (this submission's sample run)
analysis_output.json         full deterministic analysis backing the report
review_state.json            human review gate state for this run
architecture.md              diagram + rationale
version1/DESIGN.md           Version 1 plan (design doc, not implemented)
```
