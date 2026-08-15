"""
Deterministic analysis layer for the GenAR PADER challenge.

Everything in this file is plain pandas/Python — no LLM calls. The output of
this module is the ONLY thing the report-generation layer is allowed to see
when it writes narrative text. If a number isn't computed here, it cannot
appear in the report.

Run standalone: python src/analysis.py path/to/data.xlsx (or .csv)
"""
import pandas as pd
import json
import sys
from datetime import datetime


def load_data(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    return df


def dedupe_cases(df: pd.DataFrame) -> pd.DataFrame:
    """One row per case (safetyreportid), keeping the first occurrence for
    case-level fields. Reaction-level analyses use the full row-level df."""
    return df.sort_values("safetyreportid").drop_duplicates(
        subset="safetyreportid", keep="first"
    )


def bucket_age(age):
    if pd.isna(age):
        return "Unknown"
    try:
        age = float(age)
    except (TypeError, ValueError):
        return "Unknown"
    if age < 2:
        return "0-1 (Neonate/Infant)"
    if age < 12:
        return "2-11 (Child)"
    if age < 18:
        return "12-17 (Adolescent)"
    if age < 65:
        return "18-64 (Adult)"
    return "65+ (Elderly)"


def run_analysis(df: pd.DataFrame) -> dict:
    cases = dedupe_cases(df)  # one row per unique case
    total_rows = len(df)
    total_cases = len(cases)

    # --- Reporting period (from data, not hardcoded) ---
    dates = pd.to_datetime(df["receivedate"].astype(str), format="%Y%m%d", errors="coerce")
    period_start = dates.min().date().isoformat() if dates.notna().any() else None
    period_end = dates.max().date().isoformat() if dates.notna().any() else None

    # --- Case volume / seriousness ---
    serious_cases = int((cases["serious"].astype(str).str.lower() == "serious").sum())
    non_serious_cases = total_cases - serious_cases

    # --- Seriousness sub-criteria (independent yes/no flags, not mutually exclusive) ---
    seriousness_flags = {}
    for col, label in [
        ("seriousnessdeath", "Death"),
        ("seriousnesslifethreatening", "Life-threatening"),
        ("seriousnesshospitalization", "Hospitalization"),
        ("seriousnessdisabling", "Disabling"),
        ("seriousnesscongenitalanomali", "Congenital anomaly"),
        ("seriousnessother", "Other medically important"),
    ]:
        if col in cases.columns:
            seriousness_flags[label] = int((cases[col].astype(str).str.lower() == "yes").sum())

    # --- Demographics (case-level) ---
    sex_counts = cases["patient_patientsex"].fillna("Unknown").value_counts().to_dict()
    cases = cases.copy()
    cases["age_bucket"] = cases["patient_patientonsetage"].apply(bucket_age)
    age_counts = cases["age_bucket"].value_counts().to_dict()

    # --- Country (occurcountry chosen as primary; noted as decision) ---
    country_counts = cases["occurcountry"].fillna("Unknown").str.title().value_counts().head(10).to_dict()

    # --- Reactions (row-level, since one case can have multiple reaction rows /
    #     multiple PTs packed in one cell) ---
    reaction_series = df["patient_reaction_reactionmeddrapt"].dropna().astype(str)
    reaction_series = reaction_series.str.split(",")
    all_reactions = [r.strip() for sub in reaction_series for r in sub if r.strip()]
    reaction_counts = pd.Series(all_reactions).value_counts()
    top_reactions = reaction_counts.head(15).to_dict()

    # Serious reactions: reactions occurring in rows where the case is serious
    serious_ids = set(cases[cases["serious"].astype(str).str.lower() == "serious"]["safetyreportid"])
    serious_rows = df[df["safetyreportid"].isin(serious_ids)]
    serious_reaction_series = serious_rows["patient_reaction_reactionmeddrapt"].dropna().astype(str).str.split(",")
    serious_reactions_flat = [r.strip() for sub in serious_reaction_series for r in sub if r.strip()]
    top_serious_reactions = pd.Series(serious_reactions_flat).value_counts().head(10).to_dict()

    # --- Outcomes (case-level, first reaction's outcome per case as a simplification) ---
    outcome_counts = cases["patient_reaction_reactionoutcome"].fillna("Unknown").value_counts().head(10).to_dict()

    # --- 15-day Alert cases (fulfillexpeditecriteria == yes) ---
    alert_cases = cases[cases["fulfillexpeditecriteria"].astype(str).str.lower() == "yes"]
    alert_count = len(alert_cases)
    alert_fatal = int((alert_cases["seriousnessdeath"].astype(str).str.lower() == "yes").sum()) if "seriousnessdeath" in alert_cases.columns else None

    # --- Trend over time: monthly case counts ---
    cases_dates = pd.to_datetime(cases["receivedate"].astype(str), format="%Y%m%d", errors="coerce")
    monthly = cases_dates.dt.to_period("M").value_counts().sort_index()
    monthly_trend = {str(k): int(v) for k, v in monthly.items()}

    # --- Case index (small sample listing, full listing goes to a CSV/table) ---
    case_index_cols = [
        "safetyreportid", "patient_reaction_reactionmeddrapt", "serious",
        "receivedate", "occurcountry", "patient_reaction_reactionoutcome",
    ]
    case_index_cols = [c for c in case_index_cols if c in cases.columns]
    case_index = cases[case_index_cols].to_dict(orient="records")

    return {
        "meta": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "source_rows": total_rows,
            "dedup_note": f"{total_rows} rows deduplicated to {total_cases} unique cases via safetyreportid",
            "country_field_used": "occurcountry (chosen over primarysource_reportercountry; usually identical, occasionally differs)",
        },
        "reporting_period": {"start": period_start, "end": period_end},
        "case_volume": {
            "total_cases": total_cases,
            "serious_cases": serious_cases,
            "non_serious_cases": non_serious_cases,
            "serious_pct": round(100 * serious_cases / total_cases, 1) if total_cases else None,
        },
        "seriousness_breakdown": seriousness_flags,
        "demographics": {
            "sex": sex_counts,
            "age_group": age_counts,
            "top_countries": country_counts,
        },
        "reactions": {
            "top_reactions_overall": top_reactions,
            "top_reactions_serious_cases": top_serious_reactions,
        },
        "outcomes": outcome_counts,
        "alert_15day": {
            "total_alert_cases": alert_count,
            "alert_fatal_cases": alert_fatal,
        },
        "monthly_trend": monthly_trend,
        "history_of_actions": None,  # explicitly: not supplied for this exercise, per Starter Guide §7
        "case_index_sample": case_index[:20],
        "case_index_full_count": len(case_index),
    }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/Bisoprolol_icsr_sample_1068rows.xlsx"
    df = load_data(path)
    result = run_analysis(df)
    print(json.dumps(result, indent=2, default=str))
