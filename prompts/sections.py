"""
Per-section prompt templates.

Each function takes the FULL analysis dict (from src/analysis.py) and returns
a *scoped* evidence packet — only the keys that section is allowed to see —
plus the instruction text for that section. This is the "context engineering"
part of the exercise: every section gets the minimum slice it needs, not the
whole analysis dump.
"""

def narrative_summary_packet(a: dict) -> dict:
    return {
        "reporting_period": a["reporting_period"],
        "case_volume": a["case_volume"],
        "top_reactions_overall": dict(list(a["reactions"]["top_reactions_overall"].items())[:5]),
        "top_countries": a["demographics"]["top_countries"],
        "outcomes": a["outcomes"],
    }

NARRATIVE_SUMMARY_INSTRUCTIONS = (
    "Write the 'Narrative Summary and Analysis' section. Cover: total cases "
    "and the serious/non-serious split, the top reported reactions, and the "
    "geographic spread. 4-6 sentences. Distinguish observed counts from any "
    "derived statement (e.g. 'most frequently reported') — do not add "
    "interpretation beyond that."
)


def case_summary_packet(a: dict) -> dict:
    return {
        "case_volume": a["case_volume"],
        "seriousness_breakdown": a["seriousness_breakdown"],
        "demographics": a["demographics"],
        "outcomes": a["outcomes"],
    }

CASE_SUMMARY_INSTRUCTIONS = (
    "Write the 'Summary Analysis of Cases' section. Cover case volume, the "
    "seriousness sub-criteria breakdown (note these are independent flags, "
    "not mutually exclusive), and demographic distribution (age, sex, "
    "country). Present as prose, citing exact figures from the packet."
)


def reaction_analysis_packet(a: dict) -> dict:
    return {
        "top_reactions_overall": a["reactions"]["top_reactions_overall"],
        "top_reactions_serious_cases": a["reactions"]["top_reactions_serious_cases"],
        "note": "No System Organ Class field is available in this dataset; "
                "analysis is at the Preferred Term level only.",
    }

REACTION_ANALYSIS_INSTRUCTIONS = (
    "Write the 'Reaction / Adverse Event Analysis' section. List the most "
    "frequently reported reactions and the most frequently reported reactions "
    "among serious cases. Explicitly state that SOC-level grouping is not "
    "available for this dataset (do not invent SOC categories)."
)


def alerts_packet(a: dict) -> dict:
    return {
        "reporting_period": a["reporting_period"],
        "alert_15day": a["alert_15day"],
        "case_volume": a["case_volume"],
    }

ALERTS_INSTRUCTIONS = (
    "Write the 'Serious Cases / 15-Day Alerts' section. State how many cases "
    "met expedited (15-day alert) criteria and, of those, how many were "
    "fatal. If nearly all serious cases also meet alert criteria, state "
    "that plainly as an observation about this dataset rather than a signal."
)


def trends_packet(a: dict) -> dict:
    return {
        "monthly_trend": a["monthly_trend"],
        "reporting_period": a["reporting_period"],
    }

TRENDS_INSTRUCTIONS = (
    "Write the 'Trends and Important Observations' section using the "
    "monthly case counts provided. Describe the shape of the trend (e.g. "
    "rising, falling, flat, or volatile) using only the numbers given. "
    "Explicitly avoid calling any pattern a 'safety signal' — present "
    "observations only, e.g. 'cases rose from X in <month> to Y in <month>.'"
)


def history_of_actions_packet(a: dict) -> dict:
    return {"history_of_actions": a["history_of_actions"]}

HISTORY_INSTRUCTIONS = (
    "Write the 'History of Actions' section. If history_of_actions is null, "
    "state explicitly that no safety-related action data was supplied for "
    "this reporting interval, and that no labeling changes, studies, or "
    "risk-minimization actions can be reported as a result. Do not invent any."
)


# Sections that are pure data (case index / cover page) skip the LLM entirely —
# they are rendered directly from the analysis dict by the report builder.
SECTIONS = [
    ("Narrative Summary and Analysis", narrative_summary_packet, NARRATIVE_SUMMARY_INSTRUCTIONS),
    ("Summary Analysis of Cases", case_summary_packet, CASE_SUMMARY_INSTRUCTIONS),
    ("Reaction/Adverse Event Analysis", reaction_analysis_packet, REACTION_ANALYSIS_INSTRUCTIONS),
    ("Serious Cases / 15-Day Alerts", alerts_packet, ALERTS_INSTRUCTIONS),
    ("Trends and Important Observations", trends_packet, TRENDS_INSTRUCTIONS),
    ("History of Actions", history_of_actions_packet, HISTORY_INSTRUCTIONS),
]
