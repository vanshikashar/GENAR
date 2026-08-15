# Version 1 — Design Note (not implemented)

Version 0 hardcodes "PADER for Bisoprolol" end to end. Here's the minimal
change set to make report type a configuration choice, not a rewrite —
without over-building for report types this exercise doesn't cover.

## 1. Section registry becomes data, not code

`prompts/sections.py` currently is Python: a fixed list of
`(name, packet_fn, instructions)`. Version 1 makes this a YAML/JSON config
per report type:

```yaml
report_type: PADER
sections:
  - name: Narrative Summary and Analysis
    requires: [case_volume, reporting_period, top_reactions_overall, top_countries, outcomes]
    instructions: "Cover total cases, serious split, top reactions, geography..."
  - name: Serious Cases / 15-Day Alerts
    requires: [alert_15day, case_volume]
    instructions: "..."
```

`requires` names keys into a single analysis dict — the packet-builder
becomes generic (`{k: analysis[k] for k in section["requires"]}`) instead of
one hand-written function per section. Adding PSUR just means writing a new
YAML file with a different section list; `generate_report.py` doesn't change.

## 2. Analyses become a registry too, decoupled from sections

Right now `analysis.py` computes everything in one `run_analysis()` call.
Version 1 splits it into named, independent analysis functions
(`total_cases()`, `serious_breakdown()`, `reactions_by_pt()`,
`monthly_trend()`...) registered in a dict. A report type's config just
lists which analyses it needs; the same `serious_breakdown()` function
serves PADER, PSUR, and PBRER without modification. This is what "reusable
analyses" in the prompt buys you concretely.

## 3. Versioning

Stamp every `report_output.md` with a small JSON sidecar:
`{dataset_hash, analysis_version, prompt_version, model, generated_at}`.
Cheap to add, makes "why did section X change between two runs" answerable
without diffing prose by eye.

## 4. Evidence tracing

Each generated sentence already ties back to one evidence packet per
section (coarse-grained). Fine-grained tracing (click a sentence, see the
exact numbers) would mean asking the model to emit inline references
(e.g. `[[case_volume.serious_cases]]`) alongside prose, then rendering those
as clickable spans. Deferred because it changes the prompt contract for
marginal value at this scale — worth doing once there's a real UI to click
into.

## 5. What survives unmodified if PSUR/PBRER/DSUR get added

- `analysis.py`'s individual analysis functions — untouched, just recombined.
- The human-review gate (`review_state.json` shape) — untouched.
- `generate_report.py`'s orchestration loop — untouched, since it already
  just iterates "sections a config gives it."
- What changes: only the YAML config per report type, and possibly new
  analysis functions for fields PADER doesn't use (e.g. PBRER's
  benefit-risk sections would need efficacy/exposure data this dataset
  doesn't have — that's a data problem, not an architecture problem).
